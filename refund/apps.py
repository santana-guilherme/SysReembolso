
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_groups(sender, **kwargs):
    from refund.models import Solicitation
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    analyst, created = Group.objects.get_or_create(name='Analyst')
    if created:
        content_type = ContentType.objects.get_for_model(Solicitation)
        perm, created = Permission.objects.get_or_create(
            name='Can view solicitation',
            codename='view_solicitation',
            content_type=content_type
        )
        analyst.permissions.add(perm)

    print('Executed group creation')


class RefundConfig(AppConfig):
    name = 'refund'

    # def ready(self) -> None:
        # post_migrate.connect(create_groups, sender=self)
