from django.db import models
from django.utils import timezone
from django.conf import settings

# seuil global (option: déplacer dans settings.py)
DEFAULT_THRESHOLD = getattr(settings, "TEMP_THRESHOLD_C", 80)

class Reading(models.Model):
    sensor_id = models.CharField(max_length=100, blank=True, null=True)
    temperature_c = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_anomaly = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # détection simple d'anomalie selon le seuil
        threshold = getattr(settings, "TEMP_THRESHOLD_C", DEFAULT_THRESHOLD)
        self.is_anomaly = self.temperature_c > threshold
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sensor_id or 'sensor'} — {self.temperature_c}°C @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
