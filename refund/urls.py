from django.urls import path, re_path
from . import views


app_name = 'refund'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.redirect_user_home, name='redirect_home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('analysis', views.analysis_queue, name='analysis_queue'),
    path('payments', views.payment_queue, name='payment_queue'),
    path('finished', views.finished_queue, name='finished_queue'),
    path('create_solicitation', views.create_solicitation,
         name='create_solicitation'),
    re_path(r'^pay_refund/(?P<refundbundle_id>\d*)',
         views.pay_refundbundle, name='pay_refund'),

    re_path(r'^update_solicitation/(?P<solicitation_id>\d*)',
         views.update_solicitation, name='update_solicitation'),
    path('analyse_solicitation/<int:solicitation_id>',
         views.analyse_solicitation, name='analyse_solicitation'),
    path(
        'solicitation_detail/<int:solicitation_id>/',
        views.solicitation_detail,
        name='solicitation_detail'
    ),
    path(
        'refundbundle_detail/<int:refundbundle_id>/',
        views.refund_bundle_detail,
        name='refundbundle_detail'
    ),
    path('refunds_by_user', views.refunds_by_user, name='refunds_by_user'),
    path('solicitations_price_by_month', views.solicitations_price_by_month,
        name='solicitations_price_by_month'),
    path('solicitations_overview_per_month',
        views.solicitations_overview_per_month, name='solicitations_overview_per_month'),
    path('solicitations_by_month',
        views.solicitations_by_month, name='solicitations_by_month'),
]
