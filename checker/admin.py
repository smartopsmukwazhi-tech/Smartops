from django.contrib import admin

from .models import CheckinSLA


@admin.register(CheckinSLA)
class CheckinSLAAdmin(admin.ModelAdmin):
    list_display = ('airline', 'aircraft_type', 'minimum_agents', 'updated_at')
    list_editable = ('minimum_agents',)
    search_fields = ('airline', 'aircraft_type')
    ordering = ('airline', 'aircraft_type')
