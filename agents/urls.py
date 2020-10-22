from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='agents/login.html')),
    path('logout', auth_views.LogoutView.as_view()),
    path('register', views.registerUser, name='registerName')
]
