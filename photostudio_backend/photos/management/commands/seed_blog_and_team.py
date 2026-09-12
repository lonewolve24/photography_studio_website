from datetime import timedelta
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from photos.models import Album, BlogPost, Photo, TeamMember


SEED_TEAM_NAMES = [
    'Awa Jallow',
    'Omar Ceesay',
    'Fatou Bah',
    'Lamin Touray',
]

SEED_POST_SLUGS = [
    'intimate-wedding-at-senegambia',
    'family-portraits-that-feel-like-home',
    'graduation-day-stories',
]


def _copy_image(source_field, dest_instance, dest_attr, filename):
    """Copy an already-uploaded image from storage (local or Spaces) onto another field."""
    source_field.open('rb')
    try:
        content = ContentFile(source_field.read())
        getattr(dest_instance, dest_attr).save(filename, content, save=True)
    finally:
        source_field.close()


def _pick(items, index):
    """Pick by index, wrapping if the list is shorter than needed."""
    if not items:
        return None
    return items[index % len(items)]


class Command(BaseCommand):
    help = (
        'Seed dummy Team Members and Blog Posts using existing uploaded photos. '
        'Safe to run on Railway after deploy so the client can preview the new sections.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete previously seeded dummy records and recreate them.',
        )

    def handle(self, *args, **options):
        photos = list(Photo.objects.exclude(image='').order_by('id'))
        if not photos:
            self.stdout.write(self.style.ERROR(
                'No uploaded photos found. Add photos in Admin first, then run this again.'
            ))
            return

        if options['force']:
            TeamMember.objects.filter(name__in=SEED_TEAM_NAMES).delete()
            BlogPost.objects.filter(slug__in=SEED_POST_SLUGS).delete()
            self.stdout.write(self.style.WARNING('Removed previous dummy team/blog records.'))

        existing_team = TeamMember.objects.filter(name__in=SEED_TEAM_NAMES).exists()
        existing_posts = BlogPost.objects.filter(slug__in=SEED_POST_SLUGS).exists()
        if (existing_team or existing_posts) and not options['force']:
            self.stdout.write(self.style.WARNING(
                'Dummy team/blog data already exists. Re-run with --force to replace it.'
            ))
            return

        self._seed_team(photos)
        self._seed_posts(photos)
        self.stdout.write(self.style.SUCCESS(
            f'Done. Team members: {TeamMember.objects.filter(name__in=SEED_TEAM_NAMES).count()} | '
            f'Blog posts: {BlogPost.objects.filter(slug__in=SEED_POST_SLUGS).count()}'
        ))
        self.stdout.write('The client can edit or replace these in Admin.')

    def _seed_team(self, photos):
        team_specs = [
            {
                'name': 'Awa Jallow',
                'role': 'Lead Photographer',
                'bio': 'Captures intimate moments with a storytelling eye.',
                'instagram': 'https://instagram.com/shotz.gm',
                'linkedin': 'https://linkedin.com',
                'twitter': 'https://twitter.com',
                'facebook': 'https://facebook.com/shotz.gm',
                'order': 1,
                'photo_index': 0,
            },
            {
                'name': 'Omar Ceesay',
                'role': 'Videographer',
                'bio': 'Cinematic coverage for weddings, events, and brands.',
                'instagram': 'https://instagram.com/shotz.gm',
                'linkedin': '',
                'twitter': '',
                'facebook': 'https://facebook.com/shotz.gm',
                'order': 2,
                'photo_index': 1,
            },
            {
                'name': 'Fatou Bah',
                'role': 'Creative Director',
                'bio': 'Shapes the visual direction from mood board to final gallery.',
                'instagram': 'https://instagram.com/shotz.gm',
                'linkedin': 'https://linkedin.com',
                'twitter': '',
                'facebook': '',
                'order': 3,
                'photo_index': 2,
            },
            {
                'name': 'Lamin Touray',
                'role': 'Editor & Retoucher',
                'bio': 'Brings polish and consistency to every deliverable.',
                'instagram': '',
                'linkedin': 'https://linkedin.com',
                'twitter': 'https://twitter.com',
                'facebook': '',
                'order': 4,
                'photo_index': 3,
            },
        ]

        for spec in team_specs:
            photo_index = spec.pop('photo_index')
            source = _pick(photos, photo_index)
            member = TeamMember(**spec, is_active=True)
            filename = Path(source.image.name).name
            _copy_image(source.image, member, 'photo', filename)
            self.stdout.write(f'  Team: {member.name} (photo index {photo_index})')

    def _seed_posts(self, photos):
        album = Album.objects.order_by('id').first()
        now = timezone.now()

        post_specs = [
            {
                'title': 'Intimate Wedding at Senegambia',
                'excerpt': 'Soft light, quiet vows, and the kind of joy you feel in every frame.',
                'body': (
                    '<p>Some weddings are loud. This one was intimate — and that made every detail matter more.</p>'
                    '<p>From the first look to the last dance, we focused on the glances, the hands, '
                    'and the in-between moments that usually get missed.</p>'
                    '<h3>What stood out</h3>'
                    '<ul><li>Golden-hour portraits</li><li>Candid ceremony reactions</li>'
                    '<li>A reception filled with colour and warmth</li></ul>'
                    '<p>If you are planning a wedding and want storytelling coverage, we would love to hear from you.</p>'
                ),
                'cover_index': 0,
                'extra_indexes': [1, 2, 3],
                'use_album': True,
                'days_ago': 12,
                'meta_title': 'Intimate Wedding Coverage | Shotz',
                'meta_description': 'A storytelling look at an intimate wedding covered by Shotz.',
            },
            {
                'title': 'Family Portraits That Feel Like Home',
                'excerpt': 'Real laughter, soft light, and a session built around connection — not stiff poses.',
                'body': (
                    '<p>Family sessions work best when everyone can relax. For this shoot we kept things simple: '
                    'natural light, familiar spaces, and room to play.</p>'
                    '<blockquote>Home is not a place. It is the people in the frame.</blockquote>'
                    '<p>Book a family session with Shotz and let us capture your season as it is.</p>'
                ),
                'cover_index': 4,
                'extra_indexes': [5, 6],
                'use_album': True,
                'days_ago': 5,
                'meta_title': 'Family Portrait Session | Shotz Stories',
                'meta_description': 'Behind a relaxed family portrait session with Shotz.',
            },
            {
                'title': 'Graduation Day Stories',
                'excerpt': 'Caps, gowns, and proud families — documenting a milestone that only happens once.',
                'body': (
                    '<p>Graduation day moves fast. Our job is to slow it down just enough to keep the pride, '
                    'the hugs, and the quiet tears.</p>'
                    '<h3>Coverage highlights</h3>'
                    '<ol><li>Pre-ceremony portraits</li><li>Walking moments and family reactions</li>'
                    '<li>Group shots that still feel personal</li></ol>'
                    '<p>Congrats to every graduate we photographed this season.</p>'
                ),
                'cover_index': 7,
                'extra_indexes': [8, 9, 10],
                'use_album': False,
                'days_ago': 2,
                'meta_title': 'Graduation Photography Stories | Shotz',
                'meta_description': 'Graduation day portraits and family moments by Shotz.',
            },
        ]

        for spec in post_specs:
            cover = _pick(photos, spec['cover_index'])
            extras = [
                _pick(photos, i)
                for i in spec['extra_indexes']
                if _pick(photos, i) and _pick(photos, i).pk != cover.pk
            ]
            extras = list({p.pk: p for p in extras}.values())

            post = BlogPost(
                title=spec['title'],
                slug=slugify(spec['title']),
                excerpt=spec['excerpt'],
                body=spec['body'],
                album=album if spec['use_album'] else None,
                meta_title=spec['meta_title'],
                meta_description=spec['meta_description'],
                published=True,
                show_on_home=True,
                published_at=now - timedelta(days=spec['days_ago']),
            )
            filename = Path(cover.image.name).name
            _copy_image(cover.image, post, 'cover_image', filename)
            if extras:
                post.extra_photos.set([p.id for p in extras])

            self.stdout.write(
                f'  Post: {post.title} (cover index {spec["cover_index"]}, '
                f'{post.extra_photos.count()} extra photos'
                f'{", album linked" if post.album_id else ""})'
            )
