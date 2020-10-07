from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import AnalysisQueue, PaymentQueue, Solicitation, RefundBundle, ItemSolicitation
from .forms import CreateItemSolicitationFormSet, SolicitationForm, AnalyseItemsSolicitationFormSet, UpdateRefundBundleForm
# Create your views here.

def index(request):
    return HttpResponse('index')


def analysis_queue(request):
    solicitations = AnalysisQueue.load().queue.all()
    return render(
        request,
        'refund/analysis_queue.html',
        {'solicitations_list': solicitations}
    )


def payment_queue(request):
    refund_bundle_list = PaymentQueue.load().queue.all()
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


def create_solicitation(request):
    if request.method == 'POST':
        form = SolicitationForm(request.POST, request.FILES)
        formset = CreateItemSolicitationFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            user = get_user_model().objects.first()
            analysis_queue_obj = AnalysisQueue.load()
            new_solicitation = analysis_queue_obj.create_solicitation(
                user,
                form.cleaned_data['claim_check'],
                form.cleaned_data['name'],
            )
            if new_solicitation is None:
                return HttpResponse('Erro')
            items = formset.save(commit=False)
            for item in items:
                item.solicitation = new_solicitation
                item.save()
            return HttpResponse('Valeu')
    else:
        formset = CreateItemSolicitationFormSet(
            prefix='items', queryset=ItemSolicitation.objects.none()
        )
        form = SolicitationForm()

    return render(
        request,
        'refund/create_solicitation.html',
        {'form': form, 'formset': formset}
    )


def analyse_solicitation(request, solicitation_id):
    if request.method == 'POST':
        formset = AnalyseItemsSolicitationFormSet(request.POST)
        solicitation = get_object_or_404(Solicitation, id=solicitation_id)
        if formset.is_valid():
            for item in formset:
                item.save()
            solicitation.authorize()
            return HttpResponse('Foi')
    else:
        solicitation = get_object_or_404(
            Solicitation, id=solicitation_id, state=0)
        formset = AnalyseItemsSolicitationFormSet(
            queryset=ItemSolicitation.objects.filter(
                solicitation=solicitation),
        )

    return render(
        request,
        'refund/analyse_solicitation.html',
        {'solicitation': solicitation, 'formset': formset}
    )


def pay_refundbundle(request, refund_bundle_id):
    if request.method == 'POST':
        form = UpdateRefundBundleForm(request.POST, request.FILES)
        if form.is_valid():
            for refund_bundle in form.save(commit=False):
                refund_bundle.finish_refund()
    else:
        form = UpdateRefundBundleForm(
            queryset=RefundBundle.objects.filter(id=refund_bundle_id)
        )

    return render(
        request,
        'refund/pay_refund.html',
        {'form': form}
    )
