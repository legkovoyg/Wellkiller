# filesapp/urls.py
from django.urls import path
from .views.filesapp_views import (
    FilesMainWindow,
    create_design_view,
    edit_design_view,
    ajax_create_design,
    get_fields_json,
    get_clusters_json,
    get_wells_json,
)

app_name = "filesapp"

urlpatterns = [
    path("", FilesMainWindow, name="files_main_window"),  # /files/
    path("create/", create_design_view, name="create_design"),
    path("edit/<uuid:design_id>/", edit_design_view, name="edit_design"),
    path("ajax_create_design/", ajax_create_design, name="ajax_create_design"),
    # Новые JSON-эндпоинты
    path("get_fields_json/", get_fields_json, name="get_fields_json"),
    path("get_clusters_json/", get_clusters_json, name="get_clusters_json"),
    path("get_wells_json/", get_wells_json, name="get_wells_json"),
]
