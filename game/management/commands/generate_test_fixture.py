from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Generates test fixture database in JSON format.'

    def handle(self, *args, **options):
        management.call_command('migrate', verbosity=0)
        User.objects.create_user(username='test_user',
                                 password='test_password')
        User.objects.create_user(username='test_user2',
                                 password='test_password2')
        management.call_command('dumpdata')
