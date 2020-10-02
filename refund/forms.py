from django.forms import ModelForm, formset_factory, modelformset_factory
from .models import Solicitation, ItemSolicitation


class SolicitationForm(ModelForm):
    class Meta:
        model = Solicitation
        fields = ['name', 'claim_check']


class ItemSolicitationForm(ModelForm):
    class Meta:
        model = ItemSolicitation
        fields = ['name', 'price']
        exclude = ()


ItemSolicitationFormSet = modelformset_factory(
    ItemSolicitation,fields=('name', 'price'))

