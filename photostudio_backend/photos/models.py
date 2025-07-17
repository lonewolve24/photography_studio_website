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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='photos')
    tags = models.ManyToManyField(Tag, blank=True, related_name='photos')
    date_uploaded = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(
        upload_to='videos/',
        validators=[
            FileExtensionValidator(['mp4', 'mov', 'avi', 'webm']),
            validate_video_size
        ]
    )
    # For video, we'll need to generate a thumbnail or poster image
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)  # Video duration
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='videos', blank=True)
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
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