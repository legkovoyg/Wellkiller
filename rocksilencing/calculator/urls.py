# calculator/urls.py

from django.urls import path
from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.calculator_page, name="home"),
    path("reagent_base/", views.reagent_base_page, name="reagent_base"),
    path("history_page/", views.history_page, name="history_page"),
    path("FAQ_page/", views.FAQ_page, name="FAQ_page"),
    path("download_report/", views.download_report, name="download_report"),
    path(
        "calculate_consumption/",
        views.calculate_consumption,
        name="calculate_consumption",
    ),
]
