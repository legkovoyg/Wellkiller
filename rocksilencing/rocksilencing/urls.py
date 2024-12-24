# rocksilencing/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView  # Импорт RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/files/", permanent=True)),
    path("calculator/", include("calculator.urls", namespace="calculator")),
    path("users/", include("users.urls", namespace="users")),
    path("files/", include("filesapp.urls", namespace="filesapp")),
    path("expert_systema/", include("expert_systema.urls", namespace="expert_systema")),
    path(
        "salt_calculator", include("salt_calculator.urls", namespace="salt_calculator")
    ),
    path("reagent_db/", include("reagent_db.urls", namespace="reagent_db")),
]
