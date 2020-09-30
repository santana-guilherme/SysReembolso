from django.shortcuts import render
from django.http import HttpResponse
from .models import AnalysisQueue, PaymentQueue, Solicitation, RefundBundle
# Create your views here.

analysis = AnalysisQueue.load()
payment = PaymentQueue.load()


def index(request):
    return HttpResponse('index')


def analysis_queue(request):
    solicitations = analysis.queue.all()
    return render(
        request,
        'refund/analysis_queue.html',
        {'solicitations_list': solicitations}
    )


def payment_queue(request):
    refund_bundle_list = payment.queue.all()
    return render(
        request,
        'refund/payment_queue.html',
        {'refund_bundle_list': refund_bundle_list}
    )


def solicitation_detail(request, solicitation_id):
    solicitation = Solicitation.objects.filter(id=solicitation_id).first()
    return render(
        request,
        'refund/solicitation_detail.html',
        {'solicitation': solicitation}
    )


def refund_bundle_detail(request, refund_bundle_id):
    refund_bundle = RefundBundle.objects.filter(id=refund_bundle_id).first()
    return render(
        request,
        'refund/refund_bundle_detail.html',
        {'refund_bundle': refund_bundle}
    )
