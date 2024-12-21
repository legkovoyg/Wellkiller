from django.db import models


class ReagentSalt(models.Model):
    name = models.CharField("Химическая формула", max_length=50)  # CaCl2, KCl и т.д.
    full_name = models.CharField("Полное название", max_length=100)
    description = models.TextField("Описание")

    def __str__(self):
        return f"{self.name} ({self.full_name})"

    class Meta:
        verbose_name = "Соль"
        verbose_name_plural = "Соли"


class ReagentSaltSolution(models.Model):
    salt = models.ForeignKey(
        ReagentSalt, on_delete=models.CASCADE, related_name="solutions"
    )
    density = models.FloatField("Плотность раствора, г/см³")
    salt_consumption = models.FloatField("Расход соли, кг/м³")
    water_consumption = models.FloatField("Расход воды, л/м³")

    def __str__(self):
        return f"{self.salt.name} - {self.density} г/см³"

    class Meta:
        verbose_name = "Раствор соли"
        verbose_name_plural = "Растворы солей"
        ordering = ["salt", "density"]  # сортировка по соли и плотности
