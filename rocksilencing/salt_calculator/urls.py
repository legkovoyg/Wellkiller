from django.urls import path
from .views.calculator import salt_calculator_page, download_scale_calc_report

app_name = "salt_calculator"

urlpatterns = [
    path("", salt_calculator_page, name="calculator"),
    path("download-report/", download_scale_calc_report, name="download_scale_report"),
]
