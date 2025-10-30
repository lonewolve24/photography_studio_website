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
    list_display = ('image_preview', 'title', 'category', 'album', 'is_featured', 'date_uploaded')
    list_filter = ('category', 'tags', 'album', 'is_featured')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview',)
    list_editable = ('is_featured',)

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
    filter_horizontal = ('categories', 'tags')
    
    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'slug', 'subtitle', 'description', 'cover_image'),
        }),
        ('Tags & Features', {
            'fields': ('tags', 'key_features'),
            'description': 'Add tags to categorize the service. Enter each key feature on a new line.'
        }),
        ('Categories', {
            'fields': ('categories',),
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
        }),
    )


class VideoAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'category', 'video_type', 'is_featured', 'date_added')
    list_filter = ('category', 'tags', 'is_featured')
    search_fields = ('title', 'description')
    readonly_fields = ('thumbnail_preview',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'tags', 'is_featured')
        }),
        ('Video Source', {
            'fields': ('video_file', 'youtube_url'),
            'description': 'Choose either upload a video file OR provide a YouTube URL (not both)'
        }),
        ('Additional Info', {
            'fields': ('thumbnail', 'duration')
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.thumbnail.url)
        return "No Thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'
    
    def video_type(self, obj):
        if obj.youtube_url:
            return format_html('<span style="color: red;">📺 YouTube</span>')
        elif obj.video_file:
            return format_html('<span style="color: green;">📁 Uploaded</span>')
        return "No Video"
    video_type.short_description = 'Type'


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Service, ServiceAdmin)

# ============================================================================
# DYNAMIC CONTENT ADMIN REGISTRATIONS
# ============================================================================

from .models import SiteSettings, SocialMediaLink, HeroSlide, AboutSection, Testimonial, Partner


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for global site settings - contact info, hours, etc."""
    fieldsets = (
        ('Contact Information', {
            'fields': ('email', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'zip_code')
        }),
        ('Business Hours', {
            'fields': ('monday_friday_open', 'monday_friday_close', 'saturday_open', 'saturday_close'),
            'description': 'Set your business operating hours'
        }),
        ('Additional Info', {
            'fields': ('tagline',),
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    """Admin for social media links"""
    list_display = ('platform_display', 'url', 'is_active', 'order')
    list_filter = ('platform', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    fieldsets = (
        (None, {
            'fields': ('platform', 'url', 'is_active', 'order')
        }),
    )
    
    def platform_display(self, obj):
        return obj.get_platform_display()
    platform_display.short_description = 'Platform'


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    """Admin for hero section slides"""
    list_display = ('image_preview', 'title', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Hero Slide Content', {
            'fields': ('title', 'subtitle', 'image', 'image_preview'),
            'description': 'Edit the title, subtitle, and upload hero image. Buttons are fixed and cannot be changed.'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at'),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; width: auto; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    """Admin for about section"""
    list_display = ('name', 'title', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    readonly_fields = ('image_preview', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'image', 'image_preview')
        }),
        ('About Content', {
            'fields': ('description', 'bio'),
            'description': 'Description appears in main section, Bio is for extended story'
        }),
        ('Company Vision & Mission', {
            'fields': ('vision', 'mission'),
            'description': 'Add your company vision and mission statements'
        }),
        ('Call-to-Action', {
            'fields': ('cta_text', 'cta_url'),
        }),
        ('Status', {
            'fields': ('is_active', 'updated_at'),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; width: auto; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'
    
    def has_add_permission(self, request):
        # Only allow one about section per person
        return True


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for client testimonials"""
    list_display = ('client_image_preview', 'client_name', 'client_type', 'rating_stars', 'is_active', 'order')
    list_filter = ('is_active', 'rating', 'client_type')
    list_editable = ('order', 'is_active')
    search_fields = ('client_name', 'client_type', 'testimonial_text')
    readonly_fields = ('client_image_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_type', 'client_image', 'client_image_preview')
        }),
        ('Testimonial Content', {
            'fields': ('testimonial_text', 'rating'),
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at'),
        }),
    )
    
    def client_image_preview(self, obj):
        if obj.client_image:
            return format_html('<img src="{}" style="height: 50px; width: 50px; border-radius: 50%; object-fit: cover;" />', obj.client_image.url)
        return "No Image"
    client_image_preview.short_description = 'Client Photo'
    
    def rating_stars(self, obj):
        return format_html(
            '<span style="color: gold;">{}</span>',
            '⭐' * obj.rating
        )
    rating_stars.short_description = 'Rating'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Admin for partners and collaborations"""
    list_display = ('logo_preview', 'name', 'category', 'is_active', 'order')
    list_filter = ('is_active', 'category')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'category')
    readonly_fields = ('logo_preview', 'created_at')
    
    fieldsets = (
        ('Partner Information', {
            'fields': ('name', 'category', 'description', 'logo', 'logo_preview')
        }),
        ('Links', {
            'fields': ('website_url',),
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'created_at'),
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height: 60px; width: auto; object-fit: contain;" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = 'Logo Preview'
