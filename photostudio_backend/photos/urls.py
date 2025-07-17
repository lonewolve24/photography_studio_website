from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/v2/', views.gallery_v2, name='gallery_v2'),
    path('services/<str:service_slug>/', views.service_detail, name='service_detail'),
]