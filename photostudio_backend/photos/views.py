import logging
import threading

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404

from .forms import ContactForm
from .models import (
    Photo, Service, Category, Video, Album,
    HeroSlide, AboutSection, Testimonial, Partner,
    SiteSettings, SocialMediaLink,
)
from .resend_email import send_contact_notification

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    """Home page with dynamic content from database"""
    # Get all active hero slides
    hero_slides = HeroSlide.objects.filter(is_active=True)
    
    # Get about section
    about_section = AboutSection.objects.filter(is_active=True).first()
    
    # Get all active testimonials
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Get all active partners
    partners = Partner.objects.filter(is_active=True)
    
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get active social media links
    social_links = SocialMediaLink.objects.filter(is_active=True)
    
    # Get featured photos for gallery preview on home page
    featured_photos = Photo.objects.filter(is_featured=True).order_by('-date_uploaded')[:15]
    
    services = Service.objects.filter(is_active=True)
    
    context = {
        'hero_slides': hero_slides,
        'about_section': about_section,
        'testimonials': testimonials,
        'partners': partners,
        'site_settings': site_settings,
        'social_links': social_links,
        'latest_photos': featured_photos,
        'services': services,
    }
    return render(request, 'photos/home.html', context)

def about(request):
    """About page with dynamic content from database"""
    about_section = AboutSection.objects.filter(is_active=True).first()
    site_settings = SiteSettings.objects.first()
    social_links = SocialMediaLink.objects.filter(is_active=True)
    
    # Get a few recent photos for the collage
    recent_photos = Photo.objects.order_by('-date_uploaded')[:4]
    
    context = {
        'about_section': about_section,
        'site_settings': site_settings,
        'social_links': social_links,
        'recent_photos': recent_photos,
    }
    return render(request, 'photos/about.html', context)


def services(request):
    # Get all active services
    services_list = Service.objects.filter(is_active=True)
    random_photo = Photo.objects.order_by('?').first()
    return render(request, 'photos/services.html', {'services': services_list, 'random_photo': random_photo})

def contact(request):
    service_choices = [
        (service.slug, service.title)
        for service in Service.objects.filter(is_active=True).order_by('order')
    ]
    form = ContactForm(request.POST or None, service_choices=service_choices)

    if request.method == 'POST':
        if form.is_valid():
            # Fire email in background — user does not wait for it
            data = dict(form.cleaned_data)
            thread = threading.Thread(
                target=send_contact_notification,
                args=(data,),
                daemon=True,
            )
            thread.start()

            # Redirect immediately with thank-you message
            messages.success(
                request,
                'Thank you! Your message has been received. We\'ll be in touch soon.',
            )
            return redirect('home')
        else:
            messages.error(request, 'Please check the form and try again.')

    return render(request, 'photos/contact.html', {'form': form})

def gallery(request):
    category_filter = request.GET.get('category')
    media_type_filter = request.GET.get('media_type')

    albums_qs = Album.objects.prefetch_related(
        Prefetch('photos', queryset=Photo.objects.select_related('category').order_by('-date_uploaded')),
        'tags',
        'photos__category',
        'cover_photo',
    )
    photos_qs = Photo.objects.select_related('category').filter(album__isnull=True).order_by('-date_uploaded')
    videos_qs = Video.objects.select_related('category').order_by('-date_added')
    
    # Apply media type filtering
    if media_type_filter == 'photos':
        videos_qs = Video.objects.none()  # Don't show videos
    elif media_type_filter == 'videos':
        albums_qs = Album.objects.none()  # Don't show albums
        photos_qs = Photo.objects.none()  # Don't show photos
    
    # Apply category filtering
    if category_filter:
        albums_qs = albums_qs.filter(photos__category__slug=category_filter).distinct()
        photos_qs = photos_qs.filter(category__slug=category_filter)
        videos_qs = videos_qs.filter(category__slug=category_filter)

    categories = Category.objects.all().order_by('name')

    # Combine into a single list for unified pagination
    all_media = list(albums_qs) + list(photos_qs) + list(videos_qs)
    
    def get_date(item):
        if hasattr(item, 'date_uploaded'):
            return item.date_uploaded
        elif hasattr(item, 'date_created'):
            return item.date_created
        elif hasattr(item, 'date_added'):
            return item.date_added
        from django.utils import timezone
        return timezone.now()

    all_media.sort(key=get_date, reverse=True)

    paginator = Paginator(all_media, 12)  # Show 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Random photo for hero banner
    random_photo = Photo.objects.order_by('?').first()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category_filter': category_filter,
        'media_type_filter': media_type_filter,
        'random_photo': random_photo,
    }
    return render(request, 'photos/gallery.html', context)

def gallery_v2(request):
    category_filter = request.GET.get('category')
    media_type_filter = request.GET.get('media_type')
    categories = Category.objects.all().order_by('name')

    albums_qs = Album.objects.prefetch_related(
        Prefetch('photos', queryset=Photo.objects.select_related('category').order_by('-date_uploaded')),
        'cover_photo',
    )

    photos_qs = Photo.objects.select_related('category').filter(album__isnull=True).order_by('-date_uploaded')
    videos_qs = Video.objects.select_related('category').order_by('-date_added')

    # Apply media type filtering
    if media_type_filter == 'photos':
        albums_qs = albums_qs
        photos_qs = photos_qs
        videos_qs = Video.objects.none()  # Don't show videos
    elif media_type_filter == 'videos':
        albums_qs = Album.objects.none()  # Don't show albums
        photos_qs = Photo.objects.none()  # Don't show photos
        videos_qs = videos_qs
    # If no media type filter, show all (default behavior)

    if category_filter:
        albums_qs = albums_qs.filter(photos__category__slug=category_filter).distinct()
        photos_qs = photos_qs.filter(category__slug=category_filter)
        videos_qs = videos_qs.filter(category__slug=category_filter)

    # materialize and attach chunks per album
    albums = list(albums_qs)
    for a in albums:
        ps = list(a.photos.all())
        a.chunks = [ps[i:i+4] for i in range(0, len(ps), 4)]

    paginator = Paginator(photos_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    banner_photos = Photo.objects.order_by('-date_uploaded')[:5]

    return render(request, 'photos/gallery_v2.html', {
        'albums': albums,
        'page_obj': page_obj,
        'categories': categories,
        'category_filter': category_filter,
        'media_type_filter': media_type_filter,
        'banner_photos': banner_photos,
        'videos': videos_qs,
    })

def service_detail(request, service_slug):
    """
    Renders a specific service page.
    - Fetches the service by its slug.
    - Gets all categories linked to this service.
    - For each category, gets the associated photos and videos filtered by service type.
    """
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    
    # Get all categories associated with this service that we will use as tabs
    service_categories = service.categories.all()

    # Determine media type filtering based on service type
    show_photos = True
    show_videos = True
    
    if service.title == "Video Production":
        show_photos = False  # Only show videos
    elif service.title in ["Photography", "Graphic Design"]:
        show_videos = False  # Only show photos
    # For other services like "Voiceover Recording", show both by default

    albums = Album.objects.prefetch_related('photos__category', 'cover_photo').filter(
        photos__category__in=service_categories
    ).distinct()

    standalone_photos = Photo.objects.select_related('category').filter(
        album__isnull=True,
        category__in=service_categories
    ).order_by('-date_uploaded')

    # build media_by_category combining albums + standalone photos
    media_by_category = {}
    for cat in service_categories:
        category_data = {
            'albums': [a for a in albums if a.category and a.category.id == cat.id] if show_photos else [],
            'photos': list(standalone_photos.filter(category=cat)) if show_photos else [],
            'videos': list(Video.objects.filter(category=cat).order_by('-date_added')) if show_videos else [],
        }
        media_by_category[cat] = category_data

    context = {
        'service': service,
        'media_by_category': media_by_category,
        'show_photos': show_photos,
        'show_videos': show_videos,
        'random_photo': Photo.objects.order_by('?').first()
    }
    
    return render(request, 'photos/service_detail.html', context)