from django.contrib import admin
from .models.technology import TechnologyGroup, Technology


@admin.register(TechnologyGroup)
class TechnologyGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("short_name", "name", "group", "density_min", "density_max")
    list_filter = (
        "group",
        "surfactants",
        "polymers",
        "weighting_agents",
        "corrosion_inhibitors",
        "scale_inhibitors",
        "reagent_salts",
    )
    search_fields = ("name", "short_name", "notes")
    filter_horizontal = (
        "surfactants",
        "polymers",
        "weighting_agents",
        "other_materials",
        "corrosion_inhibitors",
        "scale_inhibitors",
        "reagent_salts",
    )
    fieldsets = (
        (None, {"fields": ("group", "name", "short_name", "notes")}),
        (
            "Компоненты",
            {
                "fields": (
                    "surfactants",
                    "polymers",
                    "weighting_agents",
                    "other_materials",
                    "corrosion_inhibitors",
                    "scale_inhibitors",
                    "reagent_salts",
                )
            },
        ),
        (
            "Характеристики",
            {
                "fields": (
                    "collector_carbonate",
                    "collector_terrigenous",
                    "temperature_min",
                    "temperature_max",
                    "pressure_anpd",
                    "pressure_npnd",
                    "pressure_nd",
                    "pressure_npvd",
                    "pressure_avpd",
                    "water_compatible",
                    "density_min",
                    "density_max",
                )
            },
        ),
    )
