from django.contrib.contenttypes import fields
from django.forms import ModelForm, modelformset_factory, modelform_factory
from django import forms
from .models import Solicitation, ItemSolicitation, RefundBundle


class SolicitationForm(ModelForm):
    class Meta:
        model = Solicitation
        fields = ['name', 'claim_check']


CreateItemSolicitationFormSet = modelformset_factory(
    ItemSolicitation, fields=('name', 'price'), extra=1)


class AnalyseItemsSolicitationForm(ModelForm):
    class Meta:
        model = ItemSolicitation
        fields = ['name', 'price','accepted']

    name = forms.CharField(disabled=True)
    price = forms.FloatField(disabled=True)


AnalyseItemsSolicitationFormSet = modelformset_factory(
  model=ItemSolicitation, form=AnalyseItemsSolicitationForm, extra=0
)

class UpdateRefundBundleModelForm(ModelForm):
    class Meta:
        model = RefundBundle
        fields = ['price', 'account_number', 'pix', 'refund_memo']
    price = forms.FloatField(disabled=True)
    account_number = forms.IntegerField(disabled=True, required=False)
    pix = forms.CharField(disabled=True, required=False)

#Apperently modelform_factory has a problem validating disabled fields
#https://stackoverflow.com/questions/19006895/django-validate-a-disabled-field-in-modelform-factory
UpdateRefundBundleForm = modelformset_factory(
  model=RefundBundle, form=UpdateRefundBundleModelForm, extra=0
)
