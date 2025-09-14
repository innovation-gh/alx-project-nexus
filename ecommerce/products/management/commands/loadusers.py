from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load user data from JSON'

    def handle(self, *args, **options):
        call_command('loaddata', 'users.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded user data'))