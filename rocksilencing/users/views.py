# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from users.forms import LoginUserForm, RegisterUserForm


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
                return redirect(
                    "filesapp:files_main_window"
                )  # Используем именованный URL
            else:
                # Добавьте сообщение об ошибке или обработку
                return render(
                    request,
                    "users/login.html",
                    {"form": form, "error": "Неверное имя пользователя или пароль."},
                )
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
            login(request, user)  # Автоматический вход после регистрации (опционально)
            return redirect("users:register_done")  # Перенаправление на страницу успеха
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html", {"form": form})


def register_done(request):
    return render(request, "users/register_done.html")
