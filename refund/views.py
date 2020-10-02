from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import AnalysisQueue, PaymentQueue, Solicitation, RefundBundle, ItemSolicitation
from .forms import ItemSolicitationFormSet, SolicitationForm
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
        formset = ItemSolicitationFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            analysis_queue_obj = AnalysisQueue.load()
            new_solicitation = analysis_queue_obj.create_solicitation(
                User.objects.first(),
                form.cleaned_data['claim_check'],
                form.cleaned_data['name'],
            )
            items = formset.save(commit=False)
            for item in items:
                item.solicitation = new_solicitation
                item.save()
            return HttpResponse('Value')
    else:
        formset = ItemSolicitationFormSet(prefix='items', queryset=ItemSolicitation.objects.none())
        form = SolicitationForm()

    return render(
      request,
      'refund/create_solicitation.html',
      {'form': form, 'formset': formset}
    )
