from django.core.management.base import BaseCommand
import csv
from bp.models import Reading
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = "Imports bps from a local CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        with open(options["file_path"], mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                ## AM
                try:
                    Reading.objects.update_or_create(
                        timestamp=timezone.make_aware(datetime.fromisoformat(row["Date"] + " 08:00:00")),
                        systolic=int(row["systolic_AM"]),
                        diastolic=int(row["diastolic_AM"]),
                        AMPM="AM",
                    )
                except:
                    pass

                try:
                ## PM
                    Reading.objects.update_or_create(
                        timestamp=timezone.make_aware(datetime.fromisoformat(row["Date"] + " 17:00:00")),
                        systolic=int(row["systolic_PM"]),
                        diastolic=int(row["diastolic_PM"]),
                        AMPM="PM",
                    )
                except:
                    pass

        self.stdout.write(self.style.SUCCESS("Import complete."))