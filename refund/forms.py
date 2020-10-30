from django.forms import ModelForm, modelformset_factory
from django import forms
from django.utils.translation import gettext as _
from .models import Solicitation, ItemSolicitation, RefundBundle



class SolicitationForm(ModelForm):

    name = forms.CharField(initial='', label=_("Name"), 
        help_text='Nome da atividade que gerou o custo')
    class Meta:
        model = Solicitation
        fields = ['name', 'claim_check']
        labels = {
            'claim_check': _("Claim check")
        }


def get_item_solicitation_formset(extra: int = 0, can_delete:bool = False):
    return modelformset_factory(
        ItemSolicitation, fields=('name', 'price'),
        extra=extra, can_delete=can_delete,
        labels={
            'name': _("Name"),
            'price': _("Price")
        }
    )


class AnalyseItemsSolicitationForm(ModelForm):
    class Meta:
        model = ItemSolicitation
        fields = ['name', 'price','accepted']
        labels = {
            'name': _("Name"),
            'price': _("Price"),
            'accepted': _("Accepted")
        }
    name = forms.CharField(disabled=True)
    price = forms.FloatField(disabled=True)


AnalyseItemsSolicitationFormSet = modelformset_factory(
  model=ItemSolicitation, form=AnalyseItemsSolicitationForm, extra=0
)

class UpdateRefundBundleModelForm(ModelForm):
    price = forms.FloatField(disabled=True, label=_("Price"))
    class Meta:
        model = RefundBundle
        fields = ['price', 'refund_memo']
        labels = {
            'price': _('Price'),
            'refund_memo': _('Refund memo')
        }

#Apperently modelform_factory has a problem validating disabled fields
#https://stackoverflow.com/questions/19006895/django-validate-a-disabled-field-in-modelform-factory
UpdateRefundBundleForm = modelformset_factory(
  model=RefundBundle, form=UpdateRefundBundleModelForm, extra=0
)
