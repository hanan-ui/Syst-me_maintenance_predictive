from django.contrib import admin
from .models import Reading

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ("sensor_id", "temperature_c", "is_anomaly", "timestamp")
    list_filter = ("is_anomaly", "sensor_id")
    search_fields = ("sensor_id",)
    readonly_fields = ("is_anomaly",)
