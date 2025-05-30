# users/urls.py

from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("register/done/", views.register_done, name="register_done"),
]
