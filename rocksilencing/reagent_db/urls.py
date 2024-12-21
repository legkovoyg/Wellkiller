from django.urls import path
from .views.reagent_db_views import reagent_db_page, calculate_consumption

app_name = "reagent_db"

urlpatterns = [
    path("", reagent_db_page, name="main"),
    path("calculate_consumption/", calculate_consumption, name="calculate_consumption"),
]
