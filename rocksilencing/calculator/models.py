from django.db import models


# Create your models here.
class Salt(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Описание соли")

    def __str__(self):
        return self.name


class Solution(models.Model):
    salt = models.ForeignKey(Salt, on_delete=models.CASCADE, related_name="solutions")
    density = models.FloatField(help_text="Плотность раствора (г/см³)")
    salt_consumption = models.FloatField(help_text="Расход соли (кг/м³)")
    water_consumption = models.FloatField(help_text="Расход пресной воды (л/м³)")

    def __str__(self):
        return f"{self.salt.name}, {self.density}, {self.salt_consumption}, {self.water_consumption}"


# f'{self.salt.name} - {self.density} г/см³'
