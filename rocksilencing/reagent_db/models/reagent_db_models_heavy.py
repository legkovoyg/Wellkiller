from django.db import models


class WeightingAgent(models.Model):
    MATERIAL_TYPES = [
        ("Минерал", "Минерал"),
        ("Осадочная порода", "Осадочная порода"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(
        max_length=100, choices=MATERIAL_TYPES, verbose_name="Тип материала"
    )
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "Утяжелитель"
        verbose_name_plural = "Утяжелители"

    def __str__(self):
        return self.name
