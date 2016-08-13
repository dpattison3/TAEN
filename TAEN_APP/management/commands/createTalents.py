from django.core.management.base import BaseCommand
from TAEN_APP.models import Talent
 
 
class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Talent.objects.filter(talent=0).exists():
            Talent.objects.create(talent=0)
        if not Talent.objects.filter(talent=1).exists():
            Talent.objects.create(talent=1)
        if not Talent.objects.filter(talent=2).exists():
            Talent.objects.create(talent=2)
        if not Talent.objects.filter(talent=3).exists():
            Talent.objects.create(talent=3)
