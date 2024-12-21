# rocksilencing/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView  # Импорт RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Добавляем перенаправление с корневого URL на /calculator/
    path("", RedirectView.as_view(url="/calculator/", permanent=True)),
    path(
        "calculator/", include("calculator.urls", namespace="calculator")
    ),  # Изменяем путь подключения калькулятора
    path("users/", include("users.urls", namespace="users")),
    path("design_management/", include("filesapp.urls", namespace="filesapp")),
    path("expert_systema/", include("expert_systema.urls", namespace="expert_systema")),
    path("api/chat/", include("calculator.chat_urls", namespace="calculator")),
    path(
        "salt_calculator", include("salt_calculator.urls", namespace="salt_calculator")
    ),
]
