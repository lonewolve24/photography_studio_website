from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Photo, Video, Album, Category

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'services', 'gallery', 'contact']

    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

class PhotoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Photo.objects.filter(is_featured=True)

    def lastmod(self, obj):
        return obj.date_added

class VideoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Video.objects.filter(is_featured=True)

    def lastmod(self, obj):
        return obj.date_added

class AlbumSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Album.objects.all()

    def lastmod(self, obj):
        return obj.date_created
