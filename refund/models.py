import logging
from django.db import models
from django.conf import settings

REFUNDBUNDLE_STATE = {
    0: 'AGUARDANDO PAGAMENTO',
    1: 'FINALIZADO'
}

SOLICITATION_STATE = {
    0: 'EM ANALISE',
    1: 'AGUARDANDO PAGAMENTO',
    2: 'FINALIZADO'
}


class RefundQueue(models.Model):
    """Base class for Queue"""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """ Singleton """
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def size(self):
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def front(self):
        return self.queue[0]

    def back(self):
        return self.queue[-1]

    def push(self, element):
        self.queue.append(element)
        return 1

    def pop(self):
        return self.queue.pop(0)


class FinishQueue(RefundQueue):
    """
    Queue responsible for storing RefundBundles that where accepted and paid.
    """

    def add_refund_bundle(self):
        pass


class AnalysisQueue(RefundQueue):
    """
    Queue responsible for group solicitations waiting for analysis.
    """

    def create_solicitation(self, user:settings.AUTH_USER_MODEL, claim_check, name=None):  # and claim_check
        """
        Create solicitation and adds to queue.
        """
        if user is not None:  # and verify if user is not a analyst
            solicitation = Solicitation(
                name=name, queue=self, user=user, claim_check=claim_check
            )
            solicitation.save()
            return solicitation
        logging.warning('Couldn\'t create solicitation because user as not passed')
        return None


class PaymentQueue(RefundQueue):

    """
    Queue responsible for gathering solicitations in RefundBundle objects
    while waiting for payment.
    """

    def add_solicitation(self, solicitation_id):
        """
        Add solicitation to refund bundle on queue.
        """
        solicitation = Solicitation.objects.filter(id=solicitation_id).first()
        refund_bundle = self.__search_for_refund_bundle(solicitation)
        refund_bundle.solicitations.add(solicitation)
        refund_bundle.price += solicitation.price
        refund_bundle.save()

    def __search_for_refund_bundle(self, solicitation):
        """
        Searches for refund bundle, if no one was found create one
        and return
        """
        refund_bundle = None
        for refund in self.queue.all():
            if solicitation.user == refund.user:
                refund_bundle = refund

        if refund_bundle is not None and refund_bundle.accepting_solicitations:
            return refund_bundle

        return self.__create_refund_bundle(solicitation.user)

    def __create_refund_bundle(self, user) -> object:
        """
        Create refund bundle with user passed in parameter, append to queue and
        returns it.
        """
        refund_bundle = RefundBundle(queue=self, user=user)
        refund_bundle.save()
        return refund_bundle


class RefundBundle(models.Model):
    """
    Collection of solicitations used to perform payment and
    store the refund memo.
    """
    price = models.FloatField(default=0)
    state = models.IntegerField(default=0)
    account_number = models.IntegerField(null=True)
    pix = models.CharField(null=True, max_length=20)
    refund_memo = models.ImageField()
    accepting_solicitations = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='refund',
        null=False,
        on_delete=models.CASCADE
    )
    queue = models.ForeignKey(
        PaymentQueue,
        null=False,
        on_delete=models.PROTECT,
        related_name='queue'
    )

    def update_price(self):
        total_price = 0
        for solicitation in self.solicitations.all():
            total_price += solicitation.price
        self.price = total_price

    def finish_refund(self):
        if self.refund_memo != None:
            try:
                for solicitation in self.solicitations.all():
                    solicitation.finalize()
                self.state = 1
                self.save()
            except RuntimeError as e:
                logging.error(str(e))


class Solicitation(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    name = models.CharField(max_length=100, default='no name')
    price = models.FloatField(default=0)
    state = models.IntegerField(default=0)
    claim_check = models.ImageField(upload_to='claim_checks/')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solicitations',
        on_delete=models.CASCADE,
        null=False
    )
    refund_bundle = models.ForeignKey(
        RefundBundle,
        related_name="solicitations",
        on_delete=models.CASCADE,
        null=True
    )
    queue = models.ForeignKey(
        AnalysisQueue,
        related_name='queue',
        null=True,
        on_delete=models.CASCADE,
        default=1
    )

    def save(self, *args, **kwargs):
        if self.id is None and not self.name:
            new_id = Solicitation.objects.aggregate(
                id_max=models.Max('id'))['id_max']
            if not new_id:
                new_id = 1
            self.name = f'Nº {new_id}'
            self.id = new_id
        super().save(*args, **kwargs)

    def update_price(self):
        total_price = 0.0
        for item in self.items.all():
            if item.accepted:
                total_price += item.price
        self.price = total_price
        self.save()

    def all_itens_resolved(self):
        for item in self.items.all():
            if item.accepted is None:
                return False
        return True

    def authorize(self):
        if self.all_itens_resolved():
            self.state = 1
            self.queue = None
            self.save()
            payment_queue = PaymentQueue.load()
            # i think is better for security
            payment_queue.add_solicitation(self.id)

    def finalize(self):
        if self.all_itens_resolved():
            if self.price > 0:  # falta verificar se refund_bundle tem uma nota fiscal
                self.state = 2
            else:
                self.state = 2
        else:
            raise RuntimeError(f'Solicitation {self.name} can\'t '
                               'be finished because there are still itens that need to be resolved')

    def get_state(self):
        return SOLICITATION_STATE[self.state]

    def add_item(self, item: object):
        """
        Add solicitation item to solicitation
        """
        self.items.append(item)


class ItemSolicitation(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    accepted = models.BooleanField(null=True)
    denied_motive = models.CharField(max_length=400, null=True)
    solicitation = models.ForeignKey(
        Solicitation, related_name="items", on_delete=models.CASCADE
    )
