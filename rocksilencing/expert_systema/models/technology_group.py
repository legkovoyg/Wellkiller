from django.db import models


class TechnologyGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название группы технологий")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа технологий"
        verbose_name_plural = "Группы технологий"
