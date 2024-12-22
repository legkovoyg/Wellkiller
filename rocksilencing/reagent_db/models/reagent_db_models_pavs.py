from django.db import models


class Surfactant(models.Model):
    PAV_TYPES = [
        ("Анионный ПАВ", "Анионный ПАВ"),
        ("Катионный ПАВ", "Катионный ПАВ"),
        ("Неионный ПАВ", "Неионный ПАВ"),
        ("Смесь анионных и катионных ПАВ", "Смесь анионных и катионных ПАВ"),
        ("Смесь анионных и неионнных ПАВ", "Смесь анионных и неионнных ПАВ"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, choices=PAV_TYPES, verbose_name="Тип ПАВ")
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "ПАВ"
        verbose_name_plural = "ПАВ"

    def __str__(self):
        return self.name
