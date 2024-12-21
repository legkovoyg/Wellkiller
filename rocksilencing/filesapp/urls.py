from django.urls import path
from . import views


app_name = "filesapp"
urlpatterns = [
    path("/main", views.FilesMainWindow, name="design_management"),
]
