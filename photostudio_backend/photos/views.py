from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Photo, Service, Category, PricingPackage, Video

# Create your views here.
def home(request):

    return render(request, 'photos/home.html')

def about(request):
    return render(request, 'photos/about.html')

def services(request):
    # Get all active services
    services_list = Service.objects.filter(is_active=True)
    return render(request, 'photos/services.html', {'services': services_list})

def service_detail(request, service_slug):
    """
    Renders a specific service page based on the service_slug.
    Most content is static (template-based) except pricing and photos.
    """
    # Get the service by slug
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    
    # Get pricing packages
    pricing_packages = PricingPackage.objects.filter(service=service).order_by('order')
    
    # Get photos for this service's category
    photos = Photo.objects.filter(category=service.category)[:12]
    
    # Get videos for this service's category
    videos = Video.objects.filter(category=service.category)[:8]
    
    context = {
        'service': service,
        'service_slug': service_slug,
        'pricing_packages': pricing_packages,
        'photos': photos,
        'videos': videos,
        'service_header_image': f'images/services/{service_slug}/header.jpg'  # Fallback
    }
    
    # Return template based on slug
    if service_slug == 'wedding':
        return render(request, 'photos/services/wedding.html', context)
    elif service_slug == 'portrait':
        return render(request, 'photos/services/portrait.html', context)
    elif service_slug == 'event':
        return render(request, 'photos/services/event.html', context)
    # Add more services as needed
    else:
        # Fallback to a generic template
        return render(request, 'photos/services/generic.html', context)