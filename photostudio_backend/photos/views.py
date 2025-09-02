from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from .models import Photo, Service, Category,  Video, Album
from django.db.models import Prefetch
from django.db.models import Q

# Create your views here.
def home(request):
    latest_photos = Photo.objects.order_by('-date_uploaded')[:9]
    services = Service.objects.filter(is_active=True)
    context = {
        'latest_photos': latest_photos,
        'services': services,
    }
    return render(request, 'photos/home.html', context)

def about(request):
    return render(request, 'photos/about.html')

def services(request):
    # Get all active services
    services_list = Service.objects.filter(is_active=True)
    return render(request, 'photos/services.html', {'services': services_list})

def contact(request):
    return render(request, 'photos/contact.html')

def gallery(request):
    category_filter = request.GET.get('category')

    albums_qs = Album.objects.prefetch_related(
        Prefetch('photos', queryset=Photo.objects.select_related('category').order_by('-date_uploaded')),
        'tags',
        'photos__category',
        'cover_photo',
    )
    photos_qs = Photo.objects.select_related('category').filter(album__isnull=True).order_by('-date_uploaded')
    
    albums = list(albums_qs)  # materialize
    for a in albums:
        ps = list(a.photos.all())
        a.chunks = [ps[i:i+4] for i in range(0, len(ps), 4)]

    if category_filter:
        albums_qs = albums_qs.filter(photos__category__slug=category_filter).distinct()
        photos_qs = photos_qs.filter(category__slug=category_filter)

    categories = Category.objects.all().order_by('name')

    context = {
        'albums': albums_qs,
        'standalone_photos': photos_qs,
        'categories': categories,
        'category_filter': category_filter,
    }
    return render(request, 'photos/gallery.html', context)

def gallery_v2(request):
    category_filter = request.GET.get('category')
    categories = Category.objects.all().order_by('name')

    albums_qs = Album.objects.prefetch_related(
        Prefetch('photos', queryset=Photo.objects.select_related('category').order_by('-date_uploaded')),
        'cover_photo',
    )

    photos_qs = Photo.objects.select_related('category').filter(album__isnull=True).order_by('-date_uploaded')

    if category_filter:
        albums_qs = albums_qs.filter(photos__category__slug=category_filter).distinct()
        photos_qs = photos_qs.filter(category__slug=category_filter)

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
        'banner_photos': banner_photos,
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
            'videos': list(Video.objects.filter(category=cat)) if show_videos else [],
        }
        media_by_category[cat] = category_data

    context = {
        'service': service,
        'media_by_category': media_by_category,
        'show_photos': show_photos,
        'show_videos': show_videos,
    }
    
    return render(request, 'photos/service_detail.html', context)