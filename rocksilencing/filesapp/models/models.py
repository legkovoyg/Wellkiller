import uuid
from django.db import models
from django.utils import timezone


class Design(models.Model):
    """
    Модель для хранения информации о "Дизайне".
    Храним общие данные и результаты из модулей:
    - Калькулятор глушения (kill_data)
    - Калькулятор солеотложений (scale_data)
    - Экспертная система (expert_data)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Общие поля (можно дополнять по необходимости)
    name = models.CharField("Название дизайна", max_length=255)
    field = models.CharField("Месторождение", max_length=255, blank=True, null=True)
    cluster = models.CharField(
        "Кустовая площадь", max_length=255, blank=True, null=True
    )
    well = models.CharField("Скважина", max_length=255, blank=True, null=True)
    calc_type = models.CharField(
        "Тип/Варианты расчётов", max_length=255, blank=True, null=True
    )

    created = models.DateTimeField("Дата создания", auto_now_add=True)
    updated = models.DateTimeField("Дата изменения", auto_now=True)

    # Результаты разных модулей
    kill_data = models.JSONField(
        "Результаты калькулятора глушения", blank=True, null=True
    )
    scale_data = models.JSONField(
        "Результаты калькулятора солеотложений", blank=True, null=True
    )
    expert_data = models.JSONField(
        "Результаты экспертной системы", blank=True, null=True
    )
    chosen_technology = models.CharField(
        "Выбранная технология", max_length=255, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} | {self.calc_type} | {self.well}"
