from .forms import CreateItemSolicitationFormSet, SolicitationForm, \
    AnalyseItemsSolicitationFormSet, UpdateRefundBundleForm
from .models import AnalysisQueue, FinishedQueue, PaymentQueue, \
    Solicitation, RefundBundle, ItemSolicitation
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.


def index(request):
    return render(
        request,
        'base.html',
        {}
    )


@login_required(login_url='/agents/login')
def analysis_queue(request):
    print("Is user authenticated", request.user.is_authenticated)
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


@login_required(login_url='/agents/login')
def finished_queue(request):
    finished_refunds = FinishedQueue.load().queue.all()
    return render(
        request,
        'refund/payment_queue.html',
        {'refund_bundle_list': finished_refunds}
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
    print(refund_bundle.solicitations.all())
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
            user = request.user
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
        {'form': form, 'formset': formset, 'action_url': '/refund/create_solicitation'}
    )


def analyse_solicitation(request, solicitation_id):
    solicitation = get_object_or_404(
            Solicitation, id=solicitation_id, state=0)
    if request.method == 'POST':
        formset = AnalyseItemsSolicitationFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            solicitation.authorize()
            return HttpResponse('Foi')
    else:
        formset = AnalyseItemsSolicitationFormSet(
            queryset=ItemSolicitation.objects.filter(
                solicitation=solicitation),
        )

    return render(
        request,
        'refund/analyse_solicitation.html',
        {'solicitation': solicitation, 'formset': formset}
    )


def update_solicitation(request, solicitation_id):
    solicitation = get_object_or_404(Solicitation, id=solicitation_id)
    if solicitation.state > 0:
        return HttpResponse('Solicitação já foi aprovada/finalizada. \
            Você não pode atualizar essa solicitação')
    if request.method == 'POST':
        form = SolicitationForm(request.POST, request.FILES, instance=solicitation)
        formset = CreateItemSolicitationFormSet(request.POST, prefix='items')
        if form.is_valid():
            solicitation = form.save()

            items = formset.save(commit=False)
            for item in items:
                item.solicitation = solicitation
                item.save()
            return redirect(f'/refund/solicitation_detail/{solicitation.id}')
    else:
        form = SolicitationForm(instance=solicitation)
        formset = CreateItemSolicitationFormSet(prefix='items', \
            queryset=ItemSolicitation.objects.filter(
                solicitation=solicitation, accepted=None
            ))
    return render(
        request,
        'refund/create_solicitation.html',
        { 'form': form, 
        'formset': formset, 
        'action_url': f'/refund/update_solicitation/{solicitation_id}' }
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


def teste_logged_user(request):
    print(request.user)
    return HttpResponse(request.user.username)
