from django.urls import path
from .views import reservoir_characteristics_view

app_name = "expert_systema"  # Пространство имён для маршрутов приложения

urlpatterns = [
    path(
        "reservoir-characteristics/",
        reservoir_characteristics_view,
        name="reservoir_characteristics",
    ),
]
