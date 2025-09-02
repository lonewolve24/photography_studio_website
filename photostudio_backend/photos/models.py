from django.db import models
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.urls import reverse

def validate_image_size(file):

    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise ValidationError("Image file too large ( > 10MB )")
    
    return file
    
def validate_video_size(file):
    max_size = 100 * 1024 * 1024  # 100 MB
    if file.size > max_size:
        raise ValidationError("Video file too large ( > 100MB )")
    
    return file

# Create your models here.
class Category(models.Model):
    name =models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/',
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                  validate_image_size
                              ]
                              )
    thumbnail = ProcessedImageField(
        upload_to='photos/thumbnails/',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 85},
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='photos')
    album = models.ForeignKey( 'Album', null=True, blank=True, on_delete=models.SET_NULL, related_name='photos' ) # keeps photos if album is deleted; they become standalonerelated_name='photos',)
    tags = models.ManyToManyField(Tag, blank=True, related_name='photos')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ['-date_uploaded']

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        from django.core.exceptions import ValidationError

        # If linked to an album, ensure same category as other photos in that album
        if self.album_id:
            existing = set(
                self.album.photos.exclude(pk=self.pk).values_list('category_id', flat=True)
            )
            # If album already has photos with a category, this photo must match that
            if existing:
                if self.category_id is None:
                    raise ValidationError({'category': 'Category is required for photos in an album.'})
                if len(existing) > 1:
                    raise ValidationError('Album already has mixed categories; fix data before adding more photos.')
                if self.category_id not in existing:
                    raise ValidationError({'category': 'All photos in an album must share the same category.'})
        


class Album(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank = True, null = True)
    cover_photo = models.OneToOneField(Photo, on_delete=models.SET_NULL, related_name='album_cover', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='albums')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title


    
    def clean(self):
        from django.core.exceptions import ValidationError

        # On add, there is no PK yet; skip reverse relation checks
        if not self.pk:
            return

        # If a cover is set, it must belong to this album
        if self.cover_photo and self.cover_photo.album_id != self.id:
            raise ValidationError({'cover_photo': 'Cover photo must belong to this album.'})

        # Enforce uniform category across existing photos (post-save check)
        category_ids = set(
            self.photos.exclude(category__isnull=True).values_list('category_id', flat=True)
        )
        if len(category_ids) > 1:
         raise ValidationError('All photos in an album must share the same category.')
        

    def get_cover(self):
          
        return self.cover_photo or self.photos.order_by('-date_uploaded').first()

    @property
    def category(self):
        """
        Derived category: returns the common category if all photos agree,
        otherwise None (or if album has no photos).
        """
        first = self.photos.select_related('category').first()
        if not first or first.category_id is None:
            return None
        base_id = first.category_id
        others = self.photos.exclude(pk=first.pk).values_list('category_id', flat=True)
        return first.category if all(cid == base_id for cid in others) else None
    
    

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(
        upload_to='videos/',
        validators=[
            FileExtensionValidator(['mp4', 'mov', 'avi', 'webm']),
            validate_video_size
        ],
        blank=True, null=True  # Make optional when using YouTube
    )
    youtube_url = models.URLField(
        blank=True, null=True,
        help_text="YouTube video URL (alternative to uploading video file)"
    )
    # For video, we'll need to generate a thumbnail or poster image
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)  # Video duration
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name='videos', blank=True)
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        super().clean()
        # Ensure either video_file or youtube_url is provided, but not both
        if not self.video_file and not self.youtube_url:
            raise ValidationError("Either upload a video file or provide a YouTube URL.")
        if self.video_file and self.youtube_url:
            raise ValidationError("Please provide either a video file OR a YouTube URL, not both.")
    
    def get_youtube_video_id(self):
        """Extract YouTube video ID from the URL"""
        if not self.youtube_url:
            return None
        
        import re
        # Handle various YouTube URL formats
        patterns = [
            r'youtube\.com/watch\?v=([^&]+)',
            r'youtu\.be/([^?]+)',
            r'youtube\.com/embed/([^?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None
    
    def get_youtube_thumbnail_url(self):
        """Get YouTube thumbnail URL"""
        video_id = self.get_youtube_video_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return None
    
    def get_video_url(self):
        """Returns the appropriate video URL (YouTube or uploaded file)"""
        if self.youtube_url:
            return self.youtube_url
        elif self.video_file:
            return self.video_file.url
        return None
    
    def is_youtube_video(self):
        """Returns True if this is a YouTube video"""
        return bool(self.youtube_url)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_added']

class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)  # For controlling display order
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # A service can be linked to multiple categories
    categories = models.ManyToManyField(Category, blank=True, related_name='services')
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'service_slug': self.slug})