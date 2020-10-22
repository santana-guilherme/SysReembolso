from django.db import models
from django.contrib.auth import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=50, null=False, default='employee')
    agency_number = models.IntegerField(null=False, default=00000)
    account_number = models.IntegerField(null=False, default=00000)
    pix = models.CharField(null=True, max_length=20)

    def show_info(self):
        return f'{self.username} {self.role}'
