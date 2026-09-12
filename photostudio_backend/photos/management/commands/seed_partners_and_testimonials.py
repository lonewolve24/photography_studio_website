from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from photos.models import Partner, Photo, Testimonial


SEED_PARTNER_NAMES = [
    'Kairaba Beach Hotel',
    'Senegambia Fashion House',
    'Atlantic Events',
    'Banjul Bridal Studio',
]

SEED_TESTIMONIAL_NAMES = [
    'Aminata & Lamin',
    'Fatou Ceesay',
    'Kunta Kinteh Lodge',
    'Mariama Jobe',
]


def _copy_image(source_field, dest_instance, dest_attr, filename):
    source_field.open('rb')
    try:
        content = ContentFile(source_field.read())
        getattr(dest_instance, dest_attr).save(filename, content, save=True)
    finally:
        source_field.close()


def _pick(items, index):
    if not items:
        return None
    return items[index % len(items)]


class Command(BaseCommand):
    help = (
        'Seed dummy Partners and Testimonials only. '
        'Does not create, update, or delete Team Members or Blog Posts.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Replace only these dummy partners/testimonials. Team and blog are never touched.',
        )

    def handle(self, *args, **options):
        photos = list(Photo.objects.exclude(image='').order_by('id'))
        if not photos:
            self.stdout.write(self.style.ERROR(
                'No uploaded photos found. Add photos in Admin first, then run this again.'
            ))
            return

        if options['force']:
            Partner.objects.filter(name__in=SEED_PARTNER_NAMES).delete()
            Testimonial.objects.filter(client_name__in=SEED_TESTIMONIAL_NAMES).delete()
            self.stdout.write(self.style.WARNING(
                'Removed previous dummy partners/testimonials. Team and blog were not changed.'
            ))

        existing_partners = Partner.objects.filter(name__in=SEED_PARTNER_NAMES).exists()
        existing_testimonials = Testimonial.objects.filter(client_name__in=SEED_TESTIMONIAL_NAMES).exists()

        if existing_partners and existing_testimonials and not options['force']:
            self.stdout.write(self.style.WARNING(
                'Dummy partners and testimonials already exist. Re-run with --force to replace them.'
            ))
            return

        if not existing_partners or options['force']:
            self._seed_partners(photos)
        else:
            self.stdout.write('  Partner dummy data already present — skipped.')

        if not existing_testimonials or options['force']:
            self._seed_testimonials(photos)
        else:
            self.stdout.write('  Testimonial dummy data already present — skipped.')

        self.stdout.write(self.style.SUCCESS(
            f'Done. Partners: {Partner.objects.filter(name__in=SEED_PARTNER_NAMES).count()} | '
            f'Testimonials: {Testimonial.objects.filter(client_name__in=SEED_TESTIMONIAL_NAMES).count()}'
        ))
        self.stdout.write('Team bios and blog posts were not touched.')

    def _seed_partners(self, photos):
        specs = [
            {
                'name': 'Kairaba Beach Hotel',
                'category': 'Wedding Venues',
                'description': 'Coastal venue partner for destination weddings.',
                'website_url': 'https://example.com',
                'order': 1,
                'logo_index': 2,
            },
            {
                'name': 'Senegambia Fashion House',
                'category': 'Fashion Brands',
                'description': 'Lookbooks, campaigns, and editorial collaborations.',
                'website_url': 'https://example.com',
                'order': 2,
                'logo_index': 5,
            },
            {
                'name': 'Atlantic Events',
                'category': 'Event Management',
                'description': 'Corporate and social event coverage partner.',
                'website_url': 'https://example.com',
                'order': 3,
                'logo_index': 8,
            },
            {
                'name': 'Banjul Bridal Studio',
                'category': 'Bridal & Beauty',
                'description': 'Bridal styling partner for wedding-day coverage.',
                'website_url': 'https://example.com',
                'order': 4,
                'logo_index': 11,
            },
        ]

        for spec in specs:
            logo_index = spec.pop('logo_index')
            source = _pick(photos, logo_index)
            partner = Partner(**spec, is_active=True)
            filename = Path(source.image.name).name
            _copy_image(source.image, partner, 'logo', filename)
            self.stdout.write(f'  Partner: {partner.name} (logo index {logo_index})')

    def _seed_testimonials(self, photos):
        specs = [
            {
                'client_name': 'Aminata & Lamin',
                'client_type': 'Wedding Clients',
                'testimonial_text': (
                    'Shotz captured our wedding with so much care. Every quiet look and joyful moment '
                    'is in the gallery. We keep going back to the photos.'
                ),
                'rating': 5,
                'order': 1,
                'photo_index': 1,
            },
            {
                'client_name': 'Fatou Ceesay',
                'client_type': 'Family Session',
                'testimonial_text': (
                    'The family shoot felt relaxed from the start. The team directed us without making '
                    'it stiff, and the pictures feel like us.'
                ),
                'rating': 5,
                'order': 2,
                'photo_index': 4,
            },
            {
                'client_name': 'Kunta Kinteh Lodge',
                'client_type': 'Corporate Client',
                'testimonial_text': (
                    'Professional, on time, and easy to work with. Our event coverage and brand images '
                    'were delivered exactly as promised.'
                ),
                'rating': 5,
                'order': 3,
                'photo_index': 7,
            },
            {
                'client_name': 'Mariama Jobe',
                'client_type': 'Portrait Client',
                'testimonial_text': (
                    'I was nervous in front of the camera, but they made it simple. The portraits are '
                    'warm, clean, and something I am proud to share.'
                ),
                'rating': 5,
                'order': 4,
                'photo_index': 10,
            },
        ]

        for spec in specs:
            photo_index = spec.pop('photo_index')
            source = _pick(photos, photo_index)
            testimonial = Testimonial(**spec, is_active=True)
            filename = Path(source.image.name).name
            _copy_image(source.image, testimonial, 'client_image', filename)
            self.stdout.write(f'  Testimonial: {testimonial.client_name} (photo index {photo_index})')
