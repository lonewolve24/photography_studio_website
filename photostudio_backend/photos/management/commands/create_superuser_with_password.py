import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    """
    Creates a superuser using environment variables for credentials.
    Example:
    ADMIN_USER=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=password python manage.py create_superuser_with_password
    """
    help = 'Creates a superuser from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USER')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Missing environment variables. Please set ADMIN_USER, ADMIN_EMAIL, and ADMIN_PASSWORD.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists. Skipping.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}".')) 