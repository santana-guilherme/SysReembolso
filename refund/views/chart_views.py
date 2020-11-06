from django.core import serializers
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.db import connection
from django.db.models import Count
from django.utils.functional import LazyObject
from refund.models import AnalysisQueue, FinishedQueue, PaymentQueue, \
    Solicitation, RefundBundle, ItemSolicitation


def refunds_by_user(request):
    refund_queryset = RefundBundle.objects.values(
        'user__first_name', 'user__last_name').annotate(
            total_refund=Sum('price'))
    data = []
    labels = []
    for entry in refund_queryset:
        labels.append(entry['user__first_name'] + ' ' + entry['user__last_name'])
        data.append(entry['total_refund'])
    return JsonResponse(data={
        'labels': labels,
        'data': data
    }, safe=False)

def solicitations_by_month(request):
    refunds = Solicitation.objects.values(
        'created__month').annotate(Sum('price'))
    labels = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
    data = [0]*12
    for entry in refunds:
        data[entry['created__month']-1] = entry['price__sum']

    return JsonResponse(data={
        'labels': labels,
        'data': data
    }, safe=False)
