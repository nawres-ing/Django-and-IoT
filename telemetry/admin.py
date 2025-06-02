from django.contrib import admin
from .models import Telemetry

@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = ('data_type', 'value', 'value2', 'unite', 'timestamp', 'status')
    list_filter = ('data_type', 'status')
    date_hierarchy = 'timestamp'

# Register your models here.
