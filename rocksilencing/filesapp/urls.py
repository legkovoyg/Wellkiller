# filesapp/urls.py

from django.urls import path
from . import views

app_name = "filesapp"

urlpatterns = [
    path("", views.FilesMainWindow, name="design_management"),  # Корневой путь
]
