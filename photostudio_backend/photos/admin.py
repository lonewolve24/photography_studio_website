from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Photo, Video, Service



class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'date_uploaded')
    list_filter = ('category', 'tags')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.thumbnail.url)
        return "No Thumbnail"
    image_preview.short_description = 'Thumbnail'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)

# Register models
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video)
admin.site.register(Service, ServiceAdmin)
