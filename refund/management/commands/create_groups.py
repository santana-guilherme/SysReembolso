from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create default groups'

    def create_analyst_group(self):
        analyst, _ = Group.objects.get_or_create(name='Analyst')

        permissions = ['view_solicitation','change_solicitation',
            'view_analysisqueue', 'view_finishedqueue']
        for permission in permissions:
            perm = Permission.objects.get(codename=permission)
            analyst.permissions.add(perm)

    def create_treasurer_group(self):
        treasurer, _ = Group.objects.get_or_create(name='Treasurer')

        permissions = ['view_refundbundle','change_refundbundle',
            'view_paymentqueue']
        for permission in permissions:
            perm = Permission.objects.get(codename=permission)
            treasurer.permissions.add(perm)

    def create_employee_group(self):
        employee, _ = Group.objects.get_or_create(name='Employee')

        permissions = ['view_solicitation', 'change_solicitation',
            'delete_solicitation', 'view_paymentqueue', 'view_refundbundle',
            'add_solicitation', 'view_analysisqueue']
        for permission in permissions:
            perm = Permission.objects.get(codename=permission)
            employee.permissions.add(perm)

    def handle(self, *args, **options):
        self.create_analyst_group()
        self.create_treasurer_group()
        self.create_employee_group()

        print('Executed group creation')
