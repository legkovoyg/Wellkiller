from django.db import models


class ScaleInhibitor(models.Model):
    """Модель для ингибиторов солеотложений"""

    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, verbose_name="Тип")
    application = models.TextField(verbose_name="Применение")

    class Meta:
        verbose_name = "Ингибитор солеотложений"
        verbose_name_plural = "Ингибиторы солеотложений"

    def __str__(self):
        return self.name
