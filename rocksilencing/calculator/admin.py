from django.contrib import admin
from .models import Salt, Solution
# Register your models here.
@admin.register(Salt)
class SaltAdmin(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('salt', 'density', 'salt_consumption', 'water_consumption')
    list_filter = ('salt', 'density')