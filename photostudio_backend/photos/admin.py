from django.contrib import admin
from .models import Category, Tag, Photo, Video, Service, ServiceFeature, PricingPackage, PackageFeature

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3

class PricingPackageInline(admin.TabularInline):
    model = PricingPackage
    extra = 1

class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 4

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceFeatureInline, PricingPackageInline]

class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'order', 'is_highlighted')
    list_filter = ('service', 'is_highlighted')
    inlines = [PackageFeatureInline]

# Register models
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Service, ServiceAdmin)
admin.site.register(PricingPackage, PricingPackageAdmin)
