from django.db import models


class OtherMaterial(models.Model):
    MATERIAL_TYPES = [
        ("Базовая жидкость", "Базовая жидкость"),
        ("Специальная добавка", "Специальная добавка"),
        ("Химический реагент", "Химический реагент"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, choices=MATERIAL_TYPES, verbose_name="Тип")
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "Прочий материал"
        verbose_name_plural = "Прочие материалы"

    def __str__(self):
        return self.name
