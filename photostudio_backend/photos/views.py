from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from .models import Photo, Service, Category,  Video

# Create your views here.
def home(request):
    latest_photos = Photo.objects.order_by('-date_uploaded')[:9]
    context = {
        'latest_photos': latest_photos,
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
    """
    Displays all photos with category filters and pagination.
    """
    # Get all photos and categories
    photo_list = Photo.objects.order_by('-date_uploaded')
    categories = Category.objects.all()
    
    # Filter by category if a category slug is provided in the URL
    category_filter = request.GET.get('category')
    if category_filter:
        photo_list = photo_list.filter(category__slug=category_filter)
        
    # Set up pagination
    paginator = Paginator(photo_list, 12)  # Show 12 photos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category_filter': category_filter, # To keep track of the active filter
    }
    
    return render(request, 'photos/gallery.html', context)

def gallery_v2(request):
    """
    Second version of the gallery page with a custom banner.
    """
    photo_list = Photo.objects.order_by('-date_uploaded')
    categories = Category.objects.all()
    
    # Photos for the banner collage
    banner_photos = photo_list[:5]
    
    # Filter by category if a category slug is provided in the URL
    category_filter = request.GET.get('category')
    if category_filter:
        photo_list = photo_list.filter(category__slug=category_filter)
        
    # Set up pagination
    paginator = Paginator(photo_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category_filter': category_filter,
        'banner_photos': banner_photos,
    }
    
    return render(request, 'photos/gallery_v2.html', context)

def service_detail(request, service_slug):
    """
    Renders a specific service page.
    - Fetches the service by its slug.
    - Gets all categories linked to this service.
    - For each category, gets the associated photos and videos.
    """
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    
    # Get all categories associated with this service that we will use as tabs
    service_categories = service.categories.all()
    
    # Prepare a dictionary to hold photos and videos grouped by category.
    # This is perfect for creating the tabbed gallery in the template.
    media_by_category = {}
    for category in service_categories:
        photos = Photo.objects.filter(category=category)
        videos = Video.objects.filter(category=category)
        # Only add the category to our dictionary if it has content
        if photos.exists() or videos.exists():
            media_by_category[category] = {
                'photos': photos,
                'videos': videos
            }

    context = {
        'service': service,
        'media_by_category': media_by_category,
    }
    
    return render(request, 'photos/service_detail.html', context)