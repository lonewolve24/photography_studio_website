# Setup Instructions - Dynamic Content System

## Quick Start

### Step 1: Create & Apply Database Migrations

```bash
cd photostudio_backend
python manage.py makemigrations photos
python manage.py migrate
```

### Step 2: Initialize Site Settings

```bash
python manage.py init_site_settings
```

This creates default contact information. Edit in admin dashboard afterward.

### Step 3: Access Admin Dashboard

1. Go to `http://localhost:8000/admin/` (or your domain)
2. Log in with admin credentials
3. You'll see new content sections in the sidebar

---

## New Models Created

### 1. **SiteSettings** - Global Contact & Hours
- Email, phone, address
- Business hours (Monday-Friday, Saturday)
- Tagline/slogan
- *Only one record allowed*

### 2. **SocialMediaLink** - Social Profiles
- Platform selection (Instagram, Facebook, YouTube, etc.)
- URL for each platform
- Order/visibility control

### 3. **HeroSlide** - Banner Images
- Title, subtitle, description
- Hero image with text overlay
- Call-to-action button (text & URL)
- Carousel support (multiple slides)

### 4. **AboutSection** - Photographer Bio
- Name, professional title
- Bio text (short & extended)
- Professional photo
- Call-to-action button

### 5. **Testimonial** - Client Reviews
- Client name & type
- Review text
- Client photo (circular display)
- Star rating (1-5)
- Carousel support

### 6. **Partner** - Collaborations
- Partner name & category
- Logo/image
- Company website URL (optional)
- Carousel support

---

## Updated Files

### Backend Changes
- ✅ `photos/models.py` - 6 new models added
- ✅ `photos/admin.py` - Beautiful admin interfaces
- ✅ `photos/views.py` - Updated home view with dynamic data
- ✅ `photos/context_processors.py` - Global template context
- ✅ Created `photos/management/commands/init_site_settings.py`

### Documentation
- ✅ `DYNAMIC_CONTENT_GUIDE.md` - Client-facing guide
- ✅ `SETUP_INSTRUCTIONS.md` - This file

### Templates
- Need to update: `photostudio_backend/templates/photos/home.html`
  (See section below)

---

## Template Updates Required

The home page template needs to be updated to display dynamic content. Here are the key sections:

### Hero Section (Carousel)
```html
<!-- Show multiple hero slides with carousel -->
{% for slide in hero_slides %}
    <!-- Display slide image with title/subtitle overlay -->
    <!-- Show CTA button if cta_text and cta_url are set -->
{% endfor %}
```

### About Section
```html
<!-- Display about_section.image and about_section.description -->
<!-- Show CTA button with about_section.cta_text -->
```

### Partners Section
```html
<!-- Display partners carousel -->
{% for partner in partners %}
    <!-- Show partner.logo with partner.name -->
    <!-- Link to partner.website_url if available -->
{% endfor %}
```

### Testimonials Section
```html
<!-- Display testimonials carousel -->
{% for testimonial in testimonials %}
    <!-- Show testimonial.client_image, client_name, testimonial_text -->
    <!-- Display rating as stars: ⭐⭐⭐⭐⭐ -->
{% endfor %}
```

### Contact Section
```html
<!-- Pull from site_settings -->
{{ site_settings.email }}
{{ site_settings.phone }}
{{ site_settings.get_full_address }}
Monday - Friday: {{ site_settings.monday_friday_open }} - {{ site_settings.monday_friday_close }}
Saturday: {{ site_settings.saturday_open }} - {{ site_settings.saturday_close }}
```

### Footer (Updated with Social Links)
```html
<!-- Display social media links -->
{% for link in social_links %}
    <a href="{{ link.url }}" target="_blank">
        <!-- Icon for link.platform -->
    </a>
{% endfor %}

<!-- Display contact info from site_settings -->
{{ site_settings.get_full_address }}
{{ site_settings.phone }}
{{ site_settings.email }}
```

---

## Admin Dashboard Overview

After logging in, you'll see these new sections:

```
PHOTOS APP
├── Categories
├── Tags
├── Photos
├── Videos
├── Services
├── Albums
│
└── DYNAMIC CONTENT
    ├── Site Settings (⚙️ Global settings)
    ├── Social Media Links (📱)
    ├── Hero Slides (🎬 Banners)
    ├── About Section (👤)
    ├── Testimonials (⭐)
    └── Partners (🤝)
```

---

## Admin Features

### Image Previews
All sections show thumbnail previews:
- Hero Slides: 100px preview
- About Section: 100px preview
- Testimonials: 50x50px circular
- Partners: 60px logo

### Bulk Actions
- **Reorder** - Change "Order" field directly
- **Toggle Active** - Activate/deactivate multiple items
- **Search** - Find items by name or content

### Validation
- Image size limits (max 10MB per file)
- Required fields enforced
- URL validation for links
- Only one SiteSettings record allowed

---

## Data Management Tips

### Site Settings
- Only ONE record allowed
- Click existing entry to edit
- Contains all global contact info
- Auto-updates footer and contact sections

### Social Media Links
- Add one link per social platform
- Set order to control display sequence
- Deactivate (uncheck "Is Active") to hide without deleting
- Supports custom URLs too

### Hero Slides
- Create multiple slides for rotating carousel
- Set lower "Order" numbers to appear first
- Leave CTA fields empty to hide button
- Use high-resolution images (1920x1080+)

### Testimonials
- Upload client photos for better credibility
- Star ratings displayed as ⭐
- Order controls carousel rotation
- Can filter by rating or client type

### Partners
- Organize by category (Wedding Venues, Fashion Brands, etc.)
- SVG logos work great with transparency
- Optional website links
- Grouped by category in display

---

## Testing

After setup, test these:

1. ✅ Admin dashboard loads all new sections
2. ✅ Can create/edit content in each section
3. ✅ Images upload correctly with previews
4. ✅ Home page displays dynamic content
5. ✅ Footer shows contact info from SiteSettings
6. ✅ Social links appear with correct URLs
7. ✅ Testimonial carousel works
8. ✅ Partner logos display correctly
9. ✅ Hero carousel rotates
10. ✅ About section shows bio & image

---

## Troubleshooting

### Migration Issues
```bash
# If migrations fail, check for model import errors
python manage.py check

# Reset migrations (dev only!)
python manage.py migrate photos zero
python manage.py migrate
```

### Admin Not Showing New Sections
- Clear browser cache
- Check that models are registered in admin.py
- Restart Django development server

### Images Not Uploading
- Check file size (max 10MB)
- Verify file format (JPG, PNG, SVG)
- Ensure MEDIA_URL and MEDIA_ROOT are configured

### Changes Not Appearing
- Clear browser cache (Ctrl+Shift+Delete)
- Check that "Is Active" is enabled
- Restart development server

---

## Production Deployment

### Before Going Live

1. **Run migrations** on production database
2. **Initialize SiteSettings** with correct contact info
3. **Upload hero images** to production
4. **Add testimonials** with client photos
5. **Add partners** with logos
6. **Configure social media** links
7. **Test all sections** on live site
8. **Monitor file sizes** and storage usage

### Environment Variables Needed
- Ensure MEDIA_ROOT and MEDIA_URL are configured
- AWS/DigitalOcean credentials if using cloud storage
- DEBUG=False in production

### Backups
- Database backups before major changes
- Image backups (especially hero images)
- Consider version control for media files

---

## Next Steps

1. ✅ Apply migrations
2. ✅ Initialize site settings
3. ✅ Update home page template (see template section above)
4. ✅ Add sample content in admin
5. ✅ Test all sections
6. ✅ Deploy to production
7. ✅ Share `DYNAMIC_CONTENT_GUIDE.md` with client

---

## Support

For questions:
- Check `DYNAMIC_CONTENT_GUIDE.md` for client usage
- Review model definitions in `photos/models.py`
- Check admin customizations in `photos/admin.py`
- Test in development first before deploying

---

**Created:** October 2025
**Version:** 1.0


