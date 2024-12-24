from django.db import models


class ReagentType(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Тип реагента"
    )  # Название типа, например, "Прочее", "ПАВ", "Полимеры"
    description = models.TextField(
        verbose_name="Описание", blank=True, null=True
    )  # Краткое описание типа (опционально)

    class Meta:
        verbose_name = "Тип реагента"
        verbose_name_plural = "Типы реагентов"

    def __str__(self):
        return self.name
