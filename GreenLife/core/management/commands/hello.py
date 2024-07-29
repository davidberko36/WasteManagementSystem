from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Says hello'

    def handle(self, *args, **options):
        self.stdout.write("Hello from custom command!")