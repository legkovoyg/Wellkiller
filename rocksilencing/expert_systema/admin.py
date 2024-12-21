from django.contrib import admin
from .models import TechnologyGroup, Technology

@admin.register(TechnologyGroup)
class TechnologyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'collector_carbonate', 'collector_terrigenous')
    list_filter = ('group',)
    search_fields = ('name',)
