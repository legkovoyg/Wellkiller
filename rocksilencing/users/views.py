from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users.forms import LoginUserForm, RegisterUserForm
from django.shortcuts import redirect

# Create your views here.


def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect("/calculator")
    else:
        form = LoginUserForm()
    return render(request, "users/login.html", {"form": form})


def logout_user(request):
    logout(request)  # Завершает сессию пользователя
    return redirect("users:login")  # Перенаправляет на страницу авторизации


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request, "users/register_done.html")
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html", {"form": form})
