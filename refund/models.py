from django.db import models
from django.contrib.auth.models import User
import logging

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

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    def delete(self):
        pass

    @classmethod
    def load(self):
        obj, _ = self.objects.get_or_create(pk=1)
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


class AnalysisQueue(RefundQueue):
    # TODO: talvez deva ter um add/create solicitation
    pass


class PaymentQueue(RefundQueue):

    def add_solicitation(self, solicitation_id):
        solicitation = Solicitation.objects.filter(id=solicitation_id).first()
        refund_bundle = self.__search_for_refund_bundle(solicitation)
        refund_bundle.solicitations.add(solicitation)  # n sei se precisa disso
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

        if refund_bundle != None and refund_bundle.accepting_solicitations:
            return refund_bundle

        # create refund bundle
        refund_bundle = RefundBundle(queue=self, user=solicitation.user)
        refund_bundle.save()
        return refund_bundle


class RefundBundle(models.Model):
    price = models.FloatField(default=0)
    state = models.IntegerField(default=0)
    account_number = models.IntegerField(null=True)
    pix = models.CharField(null=True, max_length=20)
    refund_memo = models.ImageField()
    accepting_solicitations = models.BooleanField(default=True)
    user = models.ForeignKey(
        User,
        related_name='refund',
        null=False,
        on_delete=models.CASCADE
    )
    queue = models.ForeignKey(
        PaymentQueue,
        null=False,
        on_delete=models.CASCADE,  # trocar isso aqui
        related_name='queue'
    )

    def setPrice(self):
        totalPrice = 0
        for solicitation in self.solicitations.all():
            totalPrice += solicitation.price
        self.price = totalPrice

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
    claim_check = models.ImageField()
    user = models.ForeignKey(
        User,
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
        null=False,
        on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        if not self.id and not self.name:
            newId = Solicitation.objects.aggregate(
                id_max=models.Max('id'))['id_max']
            if not newId:
                newId = 1
            self.name = f'Nº {newId}'
            self.id = newId
        super().save(*kwargs)

    def updatePrice(self):
        totalPrice = 0.0
        for item in self.items.all():
            if item.accepted:
                totalPrice += item.price
        self.price = totalPrice
        self.save()

    def all_itens_resolved(self):
        for item in self.items.all():
            if item.accepted == None:
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

    def __add_to_refund_bundle(self, refund_bundle):
        refund_bundle.solicitations.create(self)
        refund_bundle.save()

    def finalize(self):
        if self.all_itens_resolved():
            if self.price > 0:  # verifica se refund_bundle tem uma nota fiscal
                self.state = 2
            else:
                self.state = 2
        else:
            raise RuntimeError(f'Solicitation {self.name} can\'t '
                               'be finished because there are still itens that need to be resolved')

    def get_state(self):
        return SOLICITATION_STATE[self.state]


class ItemSolicitation(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    accepted = models.BooleanField(null=True)
    denied_motive = models.CharField(max_length=400, null=True)
    solicitation = models.ForeignKey(
        Solicitation, related_name="items", on_delete=models.CASCADE
    )
