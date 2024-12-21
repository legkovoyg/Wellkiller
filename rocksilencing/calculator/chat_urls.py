# calculator/chat_urls.py

from django.urls import path
from .chat_views import chat_api

app_name = "calculator"

urlpatterns = [
    path("", chat_api, name="chat_api"),
]
