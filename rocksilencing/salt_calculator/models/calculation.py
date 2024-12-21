from django.db import models


class CalculationResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    part_of_mixture = models.FloatField()
    barit = models.FloatField()
    celestine = models.FloatField()
    anhydrate = models.FloatField()
    bassanit = models.FloatField()
    gips = models.FloatField()
    magnium_sulfat = models.FloatField()
    calcit = models.FloatField()

    class Meta:
        ordering = ["-created_at"]
