from django.db import models


class Surfactant(models.Model):
    """Модель для ПАВ"""

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, verbose_name="Тип")
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "ПАВ"
        verbose_name_plural = "ПАВы"

    def __str__(self):
        return self.name
