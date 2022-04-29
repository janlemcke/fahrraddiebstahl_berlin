import background_task.models
from django.core.management.base import BaseCommand
from background_task import background

class Command(BaseCommand):
    help = 'Set background tasks.'

    def handle(self, *args, **kwargs):
        print("#Tasks:", background_task.models.Task.objects.all().count())