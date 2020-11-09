from datetime import datetime
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.db.models import Count
from refund.models import AnalysisQueue, FinishedQueue, PaymentQueue, \
    Solicitation, RefundBundle, ItemSolicitation


def refunds_by_user(request):  # TODO: colocar data na model de refund bundle
    """
        return the total price of users refund
    """
    refund_queryset = RefundBundle.objects.values(
        'user__first_name', 'user__last_name').annotate(
            total_refund=Sum('price'))
    data = []
    labels = []
    for entry in refund_queryset:
        labels.append(entry['user__first_name'] +
                      ' ' + entry['user__last_name'])
        data.append(entry['total_refund'])
    return JsonResponse(data={
        'labels': labels,
        'data': data
    }, safe=False)


def solicitations_by_month(request):
    solicitations = Solicitation.objects.values('created__month').annotate(
        num_solicitations=Count('name'))
    labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    data = [0]*12
    for entry in solicitations:
        data[entry['created__month']-1] = entry['num_solicitations']

    return JsonResponse(data={
        'labels': labels,
        'data': data
    }, safe=False)


def solicitations_price_by_month(request):
    solicitations = Solicitation.objects.values(
        'created__month').annotate(Sum('price'))
    labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    data = [0]*12
    for entry in solicitations:
        data[entry['created__month']-1] = entry['price__sum']

    return JsonResponse(data={
        'labels': labels,
        'data': data
    }, safe=False)


def solicitations_by_user_by_month(request):
    """
        return the total price of users solicitations in the current month
    """
    refund_queryset = RefundBundle.objects.values(
        'user__first_name', 'user__last_name').annotate(
            total_refund=Sum('price'))
    data = []
    labels = []
    for entry in refund_queryset:
        labels.append(entry['user__first_name'] +
                      ' ' + entry['user__last_name'])
        data.append(entry['total_refund'])
    return JsonResponse(data={
        'labels': labels,
        'data': data
    }, safe=False)


def solicitations_overview_per_month(request):
    current_month = datetime.now().month
    solicitations = Solicitation.objects.filter(updated__month=current_month).values(
        'state').annotate(num_solicitations=Count('name'))

    labels = ['Em análise', 'Aguardando pagamento', 'Finalizada']
    data = [0] * 3

    for entry in solicitations:
        data[entry['state']] = entry['num_solicitations']

    return JsonResponse(data={
        'labels': labels,
        'data': data
    })
