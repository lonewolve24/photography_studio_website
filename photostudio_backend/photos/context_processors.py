from .models import Service

def common_data(request):
    """
    Provides common data, like the list of active services, to all templates.
    """
    active_services = Service.objects.filter(is_active=True).order_by('order')
    return {
        'active_services': active_services
    } 