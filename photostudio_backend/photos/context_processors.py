from .models import Service, SiteSettings, SocialMediaLink

def common_data(request):
    """
    Provides common data to all templates:
    - Active services
    - Site settings (contact info, hours)
    - Social media links
    """
    active_services = Service.objects.filter(is_active=True).order_by('order')
    site_settings = SiteSettings.objects.first()
    social_links = SocialMediaLink.objects.filter(is_active=True).order_by('order')
    
    return {
        'active_services': active_services,
        'site_settings': site_settings,
        'social_links': social_links,
    } 