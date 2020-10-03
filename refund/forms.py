from django.forms import ModelForm, formset_factory, modelformset_factory
from .models import Solicitation, ItemSolicitation


class SolicitationForm(ModelForm):
    class Meta:
        model = Solicitation
        fields = ['name', 'claim_check']


CreateItemSolicitationFormSet = modelformset_factory(
    ItemSolicitation,fields=('name', 'price'))

UpdateItemsSolicitationFormSet = modelformset_factory(
  ItemSolicitation, fields=('name', 'price', 'accepted')
)