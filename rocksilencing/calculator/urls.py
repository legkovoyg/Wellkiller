# calculator/urls.py

from django.urls import path
from .views import views
from .views.chat_views import chat_api

app_name = "calculator"

urlpatterns = [
    path("", views.calculator_page, name="home"),
    path("FAQ_page/", views.FAQ_page, name="FAQ_page"),
    path("download_report/", views.download_report, name="download_report"),
    path("api/chat/", chat_api, name="chat_api"),
]
