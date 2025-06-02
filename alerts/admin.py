from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('device', 'severity', 'message', 'status', 'timestamp')
    list_filter = ('severity', 'status')
    date_hierarchy = 'timestamp'

# Register your models here.
