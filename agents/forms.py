from django.forms import ModelForm, PasswordInput, CharField, ModelChoiceField
from .models import User
from django.contrib.auth.models import Group

class UserRegistrationForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','password',
        'agency_number', 'account_number', 'pix', 'email','groups']

    pix = CharField(max_length=20, required=False)
    password = CharField(max_length=50, widget=PasswordInput)
    groups = ModelChoiceField(queryset=Group.objects.all())
