from django.contrib import admin
from bp.models import Reading, Annotations

class BPAdminSite(admin.AdminSite):
    site_header = "Baba BP Admin"

bpAdminSite = BPAdminSite(name='Baba BP Admin')


class ReadingAdmin(admin.ModelAdmin):
    list_display = ["systolic", "diastolic", "timestamp", "AMPM"]

class AnnotationsAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "annotation"]

bpAdminSite.register(Annotations, AnnotationsAdmin)
bpAdminSite.register(Reading, ReadingAdmin)

