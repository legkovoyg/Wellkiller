from django.db import models


class CorrosionInhibitor(models.Model):
    """Модель для ингибиторов коррозии"""

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, verbose_name="Тип")
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "Ингибитор коррозии"
        verbose_name_plural = "Ингибиторы коррозии"

    def __str__(self):
        return self.name
