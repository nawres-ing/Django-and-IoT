from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'topic', 'is_active')
    list_filter = ('device_type', 'is_active')
    search_fields = ('name', 'topic')
