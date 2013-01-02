from django.core.management import BaseCommand
from gametex.models import GameTeXObject, GameTeXField, GameTeXFieldValue, GameTeXClass
from gametex.import
__author__ = 'cternus'

class Command(BaseCommand):
    args = '<path to JSON file> [--clear]'
    help = 'Load data from a GameTeX JSON file.'

    def handle(self, *args, **options):
        clear = 'clear' in options
        if clear:
            GameTeXFieldValue.objects.all().delete()
            GameTeXField.objects.all().delete()
            GameTeXObject.objects.all().delete()
            GameTeXClass.objects.all().delete()
