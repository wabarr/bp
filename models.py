from django.db import models
from datetime import datetime
from django.utils import timezone

class Reading(models.Model):
    systolic = models.PositiveIntegerField(help_text="top number - arterial pressure when heart contracts")
    diastolic = models.PositiveIntegerField(help_text="bottom number - arterial pressure when heart refills")
    timestamp = models.DateTimeField(default=datetime.now)
    AMPM = models.CharField(max_length=2, null=True, blank=True, choices=[("AM", "AM"), ("PM", "PM")])

    def __str__(self):
        return f'{self.systolic}/{self.diastolic} @ {self.timestamp}'

    #def save(self, *args, **kwargs):
    #    local_dt = timezone.localtime(self.timestamp)
    #    self.AMPM = local_dt.strftime('%p')
    #    super().save(*args, **kwargs)

class Annotations(models.Model):
    annotation = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
