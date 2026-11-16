from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone

class Reading(models.Model):
    systolic = models.PositiveIntegerField(help_text="top number - arterial pressure when heart contracts")
    diastolic = models.PositiveIntegerField(help_text="bottom number - arterial pressure when heart refills")
    timestamp = models.DateTimeField(default=datetime.now)
    AMPM = models.CharField(max_length=2, null=True, blank=True, choices=[("AM", "AM"), ("PM", "PM")])

    def __str__(self):
        return f'{self.systolic}/{self.diastolic} @ {self.timestamp}'

    def save(self, *args, **kwargs):
        local_dt = timezone.localtime(self.timestamp)
        if self.AMPM == "AM":
            self.timestamp = local_dt + timedelta(hours=8)
        if self.AMPM == "PM":
            self.timestamp = local_dt + timedelta(hours=17)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["timestamp", "AMPM"],
                name="single_reading_per_interval_constraint",
            )
        ]

class Annotations(models.Model):
    annotation = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "Annotation"
        verbose_name_plural = "Annotations"