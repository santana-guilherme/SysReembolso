from datetime import datetime
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.db.models import Count
from random import choice
from refund.models import AnalysisQueue, FinishedQueue, PaymentQueue, \
    Solicitation, RefundBundle, ItemSolicitation


def get_random_colors_array(num_colors):
    colors_arr = []
    for x in range(num_colors):
        colors_arr.append(generate_color())

    return colors_arr

def generate_color():
    opts = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    final_color = '#'
    for x in range(6):
        el = choice(opts)
        final_color+=el
    return final_color

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

    colors = get_random_colors_array(len(labels))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors': colors
    }, safe=False)


def solicitations_by_month(request):
    solicitations = Solicitation.objects.values('created__month').annotate(
        num_solicitations=Count('name'))
    labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    data = [0]*12
    for entry in solicitations:
        data[entry['created__month']-1] = entry['num_solicitations']

    colors = get_random_colors_array(1)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors': colors
    }, safe=False)


def solicitations_price_by_month(request):
    solicitations = Solicitation.objects.values(
        'created__month').annotate(Sum('price'))
    labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    data = [0]*12
    for entry in solicitations:
        data[entry['created__month']-1] = entry['price__sum']

    colors = get_random_colors_array(len(labels))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors': colors
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
    colors = get_random_colors_array(len(labels))
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors':colors
    }, safe=False)


def solicitations_overview_per_month(request):
    current_month = datetime.now().month
    solicitations = Solicitation.objects.filter(updated__month=current_month).values(
        'state').annotate(num_solicitations=Count('name'))

    labels = ['Em análise', 'Aguardando pagamento', 'Finalizada']
    data = [0] * 3

    for entry in solicitations:
        data[entry['state']] = entry['num_solicitations']
    
    colors = get_random_colors_array(len(labels))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors': colors
    })
