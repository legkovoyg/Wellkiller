from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users.forms import LoginUserForm
# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'],
                                password = cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect("/users/logout")
    else:
        form = LoginUserForm()

    return render(request, 'users/login.html',{"form" : form})

def logout_user(request):
    return HttpResponse('logout')