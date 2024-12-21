from django.urls import path
from filesapp.views.filesapp_views import FilesMainWindow

app_name = "filesapp"

urlpatterns = [
    path("", FilesMainWindow, name="design_management"),  # Корневой путь
]
