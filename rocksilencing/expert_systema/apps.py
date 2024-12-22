# expert_systema/apps.py

from django.apps import AppConfig


class ExpertSystemaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expert_systema"

    def ready(self):
        # Инициализация сигналов или других компонентов
        pass
