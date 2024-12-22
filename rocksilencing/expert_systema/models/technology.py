from django.db import models
from .technology_group import TechnologyGroup


class Technology(models.Model):
    group = models.ForeignKey(
        TechnologyGroup,
        on_delete=models.CASCADE,
        related_name="technologies",
        verbose_name="Группа технологий",
    )
    name = models.CharField(max_length=255, verbose_name="Название технологии")
    short_name = models.CharField(
        max_length=100, verbose_name="Краткое название", blank=True
    )
    notes = models.TextField(verbose_name="Примечания", blank=True)

    # Связи с компонентами
    surfactants = models.ManyToManyField(
        "reagent_db.Surfactant", blank=True, verbose_name="ПАВ"
    )
    polymers = models.ManyToManyField(
        "reagent_db.Polymer", blank=True, verbose_name="Полимеры"
    )
    weighting_agents = models.ManyToManyField(
        "reagent_db.WeightingAgent", blank=True, verbose_name="Утяжелители"
    )
    other_materials = models.ManyToManyField(
        "reagent_db.OtherMaterial", blank=True, verbose_name="Прочие компоненты"
    )
    corrosion_inhibitors = models.ManyToManyField(
        "reagent_db.CorrosionInhibitor", blank=True, verbose_name="Ингибиторы коррозии"
    )
    scale_inhibitors = models.ManyToManyField(
        "reagent_db.ScaleInhibitor", blank=True, verbose_name="Ингибиторы солеотложений"
    )
    reagent_salts = models.ManyToManyField(
        "reagent_db.ReagentSalt", blank=True, verbose_name="Соли"
    )

    # Существующие поля
    collector_carbonate = models.SmallIntegerField(
        verbose_name="Применимость в карбонатных коллекторах"
    )
    collector_terrigenous = models.SmallIntegerField(
        verbose_name="Применимость в терригенных коллекторах"
    )
    temperature_min = models.FloatField(
        null=True, blank=True, verbose_name="Минимальная температура"
    )
    temperature_max = models.FloatField(
        null=True, blank=True, verbose_name="Максимальная температура"
    )
    pressure_anpd = models.SmallIntegerField(verbose_name="Применимость при АНПД")
    pressure_npnd = models.SmallIntegerField(verbose_name="Применимость при НПонД")
    pressure_nd = models.SmallIntegerField(verbose_name="Применимость при НД")
    pressure_npvd = models.SmallIntegerField(verbose_name="Применимость при НПовД")
    pressure_avpd = models.SmallIntegerField(verbose_name="Применимость при АВПД")
    water_compatible = models.BooleanField(
        verbose_name="Совместимость с водочувствительными коллекторами"
    )
    density_min = models.FloatField(
        null=True, blank=True, verbose_name="Минимальная плотность"
    )
    density_max = models.FloatField(
        null=True, blank=True, verbose_name="Максимальная плотность"
    )

    def __str__(self):
        return self.short_name or self.name

    class Meta:
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"


class ReservoirCharacteristics(models.Model):
    ROCK_TYPE_CHOICES = [
        ("sandstone", "Песчаник"),
        ("carbonate", "Карбонат"),
    ]

    PRESSURE_COEFFICIENT_CHOICES = [
        ("less_0.8", "Аномально низкое пластовое давление (0.8-)"),
        ("0.8_1", "Нормальное пониженное давление (0.8-1)"),
        ("1-1.1", "Нормальное (1 - 1.1)"),
        ("1_1.3", "Нормальное повышенное давление (1.1-1.3)"),
        ("more_1.3", "Аномально высокое пластовое давление (1.3+)"),
    ]

    rock_type = models.CharField(
        max_length=20, choices=ROCK_TYPE_CHOICES, verbose_name="Тип породы коллектора"
    )
    pressure_coefficient = models.CharField(
        max_length=20,
        choices=PRESSURE_COEFFICIENT_CHOICES,
        verbose_name="Коэффициент аномальности пластового давления",
    )
    temperature = models.FloatField(verbose_name="Пластовая температура, °C")
    is_water_sensitive = models.BooleanField(verbose_name="Является водочувствительным")

    def __str__(self):
        return f"Коллектор: {self.rock_type}, Температура: {self.temperature}°C"
