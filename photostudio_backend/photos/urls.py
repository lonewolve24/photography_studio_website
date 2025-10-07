from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/v2/', views.gallery, name='gallery_v2'),
    path('services/<str:service_slug>/', views.service_detail, name='service_detail'),
    path('seo-checklist/', TemplateView.as_view(template_name='seo_checklist.html'), name='seo_checklist'),
]