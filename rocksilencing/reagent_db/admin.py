from django.contrib import admin
from reagent_db.models.reagent_db_models_salts import (
    ReagentSalt,
    ReagentSaltSolution,
)
from reagent_db.models.reagent_db_models_ingcorr import CorrosionInhibitor
from reagent_db.models.reagent_db_models_ingsalt import ScaleInhibitor
from reagent_db.models.reagent_db_models_pavs import Surfactant


class ReagentSaltSolutionInline(admin.TabularInline):
    model = ReagentSaltSolution
    extra = 1


@admin.register(ReagentSalt)
class ReagentSaltAdmin(admin.ModelAdmin):
    list_display = ["name", "full_name"]
    search_fields = ["name", "full_name"]
    inlines = [ReagentSaltSolutionInline]


@admin.register(ReagentSaltSolution)
class ReagentSaltSolutionAdmin(admin.ModelAdmin):
    list_display = ["salt", "density", "salt_consumption", "water_consumption"]
    list_filter = ["salt"]
    search_fields = ["salt__name", "salt__full_name"]


@admin.register(Surfactant)
class SurfactantAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "application")
    search_fields = ("name", "type")
    list_filter = ("type",)


@admin.register(ScaleInhibitor)
class ScaleInhibitorAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "application")
    search_fields = ("name", "type")
    list_filter = ("type",)


@admin.register(CorrosionInhibitor)
class CorrosionInhibitorAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "application")
    search_fields = ("name", "type")
    list_filter = ("type",)
