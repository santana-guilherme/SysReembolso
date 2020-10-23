from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analysis', views.analysis_queue, name='analysis_queue'),
    path('payment', views.payment_queue, name='payment_queue'),
    path('finished', views.finished_queue, name='finished_queue'),
    path('user', views.teste_logged_user, name='logged_user'),
    path('create_solicitation', views.create_solicitation,
         name='create_solicitation'),
    re_path(r'^pay_refund/(?P<refund_bundle_id>\d*)',
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
        'refund_bundle_detail/<int:refund_bundle_id>/',
        views.refund_bundle_detail,
        name='refund_bundle_detail'
    )
]
