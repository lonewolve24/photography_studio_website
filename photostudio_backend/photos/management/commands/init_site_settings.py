from django.core.management.base import BaseCommand
from photos.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize site settings with default values'

    def handle(self, *args, **options):
        if SiteSettings.objects.exists():
            self.stdout.write(self.style.WARNING('Site settings already exist. Skipping initialization.'))
            return
        
        site_settings = SiteSettings.objects.create(
            email='hello@photostudio.com',
            phone='(123) 456-7890',
            address_line1='123 Photography Lane',
            address_line2='',
            city='Creative District',
            state='NY',
            zip_code='10001',
            tagline='The Intimate Multimedia Brand',
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Site settings initialized successfully!'))
        self.stdout.write(f'  Email: {site_settings.email}')
        self.stdout.write(f'  Phone: {site_settings.phone}')
        self.stdout.write(f'  Address: {site_settings.get_full_address()}')
        self.stdout.write('\nPlease log in to the admin dashboard to update these details.')


