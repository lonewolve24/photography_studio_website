from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Photo, Video, Service, Album


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_created')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PhotoInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Limit cover choices to photos in this album
            form.base_fields['cover_photo'].queryset = Photo.objects.filter(album=obj)
        return form


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'album', 'date_uploaded')
    list_filter = ('category', 'tags', 'album')
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


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video)
admin.site.register(Service, ServiceAdmin)
