from django.db import models


class Polymer(models.Model):
    POLYMER_TYPES = [
        ("Водорастворимый полимер", "Водорастворимый полимер"),
        ("Природный полимер", "Природный полимер"),
        ("Биополимер", "Биополимер"),
        ("Синтетический полимер", "Синтетический полимер"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(
        max_length=100, choices=POLYMER_TYPES, verbose_name="Тип полимера"
    )
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "Полимер"
        verbose_name_plural = "Полимеры"

    def __str__(self):
        return self.name
