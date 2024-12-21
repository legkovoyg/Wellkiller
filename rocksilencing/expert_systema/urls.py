# expert_systema/urls.py

from django.urls import path
from . import views

app_name = "expert_systema"

urlpatterns = [
    path("", views.reservoir_characteristics_view, name="reservoir_characteristics"),
]
