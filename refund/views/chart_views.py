from django.core import serializers
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.db import connection
from django.db.models import Count
from refund.models import AnalysisQueue, FinishedQueue, PaymentQueue, \
    Solicitation, RefundBundle, ItemSolicitation


def refund_by_user(request):
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
