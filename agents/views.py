from django.db import connections
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserRegistrationForm
# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            group = form.cleaned_data['groups']
            user.save()
            group.user_set.add(user)
            group.save()
            return redirect('agents:login')
    else:
        form = UserRegistrationForm()
    return render(
        request,
        'agents/register_user.html',
        {'form': form}
    )
