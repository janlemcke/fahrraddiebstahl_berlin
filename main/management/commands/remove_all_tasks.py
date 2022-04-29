import background_task.models
from django.core.management.base import BaseCommand
from background_task import background


class Command(BaseCommand):
    help = 'Delete all background tasks.'

    def handle(self, *args, **kwargs):
        number = background_task.models.Task.objects.all().count()
        print("#Tasks:", number)
        background_task.models.Task.objects.all().delete()
        background_task.models.CompletedTask.objects.all().delete()
        number = background_task.models.Task.objects.all().count()
        print("#Tasks after delete:", number)
