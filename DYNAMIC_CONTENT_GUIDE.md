# Dynamic Content Management Guide

This guide explains how to use the new dynamic content system to manage your photography studio website without touching code.

## Overview

All content is now managed through the **Django Admin Dashboard**. Your client can log in and edit:

- ✅ **Hero Section** - Banner images with text and CTAs
- ✅ **About Section** - Personal bio and photo
- ✅ **Testimonials** - Client reviews with ratings
- ✅ **Partners** - Collaboration logos and links
- ✅ **Contact Info** - Address, phone, email, business hours
- ✅ **Social Media Links** - Instagram, Facebook, YouTube, etc.

---

## Getting Started

### 1. Create Database Migrations

After pulling the code, run:

```bash
python manage.py makemigrations photos
python manage.py migrate
```

### 2. Initialize Site Settings

Run this command to create default site settings:

```bash
python manage.py init_site_settings
```

### 3. Access the Admin Dashboard

1. Go to `http://yourdomain.com/admin/`
2. Log in with admin credentials
3. Look for new sections in the sidebar:
   - **Site Settings**
   - **Social Media Links**
   - **Hero Slides**
   - **About Section**
   - **Testimonials**
   - **Partners**

---

## Managing Each Section

### Site Settings (Global Contact Info & Hours)

**Path:** Admin Dashboard → Site Settings

This is where you set information that appears in:
- Footer on all pages
- Contact section on home page
- Any page that references contact info

**Fields:**
- **Email** - Primary contact email
- **Phone** - Main phone number
- **Address Line 1** - Street address
- **Address Line 2** - Apartment/Suite (optional)
- **City, State, Zip** - Location info
- **Business Hours** - Monday-Friday and Saturday hours
- **Tagline** - "The Intimate Multimedia Brand" or custom text

**Note:** Only ONE site settings record can exist. Edit the existing one, don't create new ones.

---

### Social Media Links

**Path:** Admin Dashboard → Social Media Links

Add links to all social media profiles.

**How to Add:**
1. Click "+ Add Social Media Link"
2. Select platform (Instagram, Facebook, Twitter, YouTube, etc.)
3. Enter the full URL (e.g., https://instagram.com/yourprofile)
4. Check "Is Active" to show it
5. Set order (lower numbers appear first)
6. Click Save

**Example URLs:**
- Instagram: `https://instagram.com/shotz_gm`
- Facebook: `https://facebook.com/shotzphoto`
- YouTube: `https://youtube.com/c/shotzphoto`
- Custom: Any URL for other platforms

---

### Hero Slides (Banner Section)

**Path:** Admin Dashboard → Hero Slides

These are the full-width banner images at the top of your home page.

**How to Add:**
1. Click "+ Add Hero Slide"
2. **Title** - Main heading (e.g., "Wedding Photography")
3. **Subtitle** - Secondary text (e.g., "Preserving your special day")
4. **Description** - Optional longer description
5. **Image** - Upload high-quality image (JPG/PNG, max 10MB)
6. **CTA Text** - Button text (e.g., "Book Now", "Learn More")
7. **CTA URL** - Where button links (e.g., `/services/`, `/gallery/`)
8. **Order** - Display order (0 shows first, supports carousel rotation)
9. Check "Is Active" to display
10. Click Save

**Tips:**
- Use high-resolution images (1920x1080 or larger)
- Keep titles short and impactful
- Order multiple slides to create a rotating carousel
- Leave CTA fields empty if you don't want a button

---

### About Section (Photographer Bio)

**Path:** Admin Dashboard → About Section

The "Hello, I'm Alex" section with personal bio.

**How to Add/Edit:**
1. Click existing entry or "+ Add About Section"
2. **Name** - Full name
3. **Title** - Professional title (e.g., "Professional Photographer")
4. **Description** - Main bio paragraph (appears in main section)
5. **Bio** - Extended story (optional)
6. **Image** - Professional photo (JPG/PNG, max 10MB)
7. **CTA Text** - Button text (default: "Read My Story")
8. **CTA URL** - Link for button (optional)
9. Check "Is Active"
10. Click Save

**Tips:**
- Use a professional portrait photo
- Write compelling description
- Keep to 2-3 paragraphs for best display

---

### Testimonials (Client Reviews)

**Path:** Admin Dashboard → Testimonials

Client testimonial carousel with photos, names, and ratings.

**How to Add:**
1. Click "+ Add Testimonial"
2. **Client Name** - Who gave the testimonial
3. **Client Type** - Category (e.g., "Wedding Clients", "Corporate Client")
4. **Testimonial Text** - The review/quote
5. **Client Image** - Optional profile picture (circular in display)
6. **Rating** - Star rating (1-5 stars)
7. **Order** - Display order in carousel
8. Check "Is Active"
9. Click Save

**Tips:**
- Include actual client quotes
- Upload client photos for better credibility
- Higher ratings appear with more stars ⭐
- Testimonials auto-rotate on homepage

---

### Partners (Collaborations)

**Path:** Admin Dashboard → Partners

Display logos of brands and organizations you work with.

**How to Add:**
1. Click "+ Add Partner"
2. **Name** - Business/brand name
3. **Category** - Type of partner (e.g., "Wedding Venues", "Fashion Brands", "Event Planners")
4. **Description** - Short description (optional)
5. **Logo** - Upload PNG/JPG/SVG image (max 10MB)
6. **Website URL** - Link to partner's website (optional)
7. **Order** - Display order
8. Check "Is Active"
9. Click Save

**Tips:**
- Use partner logos/images with transparent backgrounds (PNG)
- Keep descriptions brief
- Organized by category automatically
- Can link to partner websites

---

## Templates & Frontend

The home page template has been updated to display all dynamic content automatically.

### Updated Home Page Sections:

1. **Hero Carousel**
   - Displays all active HeroSlide objects
   - Rotates through multiple slides if available
   - Shows title, subtitle, and CTA button

2. **About Section**
   - Shows active AboutSection with image and bio
   - Features "Read My Story" or custom CTA

3. **Partners Slider**
   - Displays active Partner logos
   - Organized by category
   - Clickable links to partner websites

4. **Testimonials Carousel**
   - Shows active testimonials with client photos
   - Displays star ratings
   - Rotates through testimonials

5. **Contact Section**
   - Pulls address from SiteSettings
   - Displays email and phone
   - Shows business hours

6. **Footer**
   - Shows address, phone, email from SiteSettings
   - Displays social media links with icons
   - All social links editable in admin

---

## Useful Admin Features

### Bulk Editing

In list views, you can:
- **Reorder items** by changing the "Order" column directly
- **Toggle visibility** by clicking "Is Active" checkbox
- **Quick search** using the search bar

### Image Previews

All admin interfaces show image previews:
- **Hero Slides** - 100px preview
- **About Section** - 100px preview
- **Testimonials** - 50x50px circular preview
- **Partners** - 60px logo preview

### Filtering & Sorting

- Filter by "Is Active" status
- Search by name or content
- Sort by creation date

---

## Database Models Reference

```
SiteSettings (1 per site)
├── email, phone, address
├── business_hours
└── tagline

SocialMediaLink (Multiple)
├── platform (Instagram, Facebook, etc.)
├── url
├── is_active
└── order

HeroSlide (Multiple)
├── title, subtitle, description
├── image
├── cta_text, cta_url
├── is_active
└── order

AboutSection (Multiple)
├── name, title
├── description, bio
├── image
├── cta_text, cta_url
├── is_active
└── updated_at

Testimonial (Multiple)
├── client_name, client_type
├── testimonial_text
├── client_image
├── rating (1-5)
├── is_active
└── order

Partner (Multiple)
├── name, category
├── description
├── logo
├── website_url
├── is_active
└── order
```

---

## Common Tasks

### Add a New Partner
1. Go to Admin → Partners
2. Click "+ Add Partner"
3. Fill in name, category, upload logo
4. Set order and activate
5. Save

### Change Business Hours
1. Go to Admin → Site Settings
2. Update Monday-Friday and Saturday hours
3. Save

### Add a Testimonial
1. Go to Admin → Testimonials
2. Click "+ Add Testimonial"
3. Enter client name, testimonial text, rating
4. Upload client photo
5. Set order and activate
6. Save

### Create a New Hero Slide
1. Go to Admin → Hero Slides
2. Click "+ Add Hero Slide"
3. Upload high-quality image
4. Enter title and call-to-action
5. Set order for carousel rotation
6. Activate and save

### Add Social Media Link
1. Go to Admin → Social Media Links
2. Click "+ Add Social Media Link"
3. Select platform
4. Paste full URL
5. Set order
6. Activate and save

---

## Tips & Best Practices

### Images
- **Hero images**: 1920x1080 or larger for best quality
- **About photo**: Square or portrait orientation works best
- **Testimonial images**: Circular presentation, so square works well
- **Partner logos**: Use transparent PNG backgrounds
- **File size**: Aim for under 5MB for faster loading

### Content
- **Keep text concise** - Long descriptions get truncated
- **Use keywords** - Include relevant terms in bios and descriptions
- **Testimonials** - Use real client quotes for authenticity
- **Partner categories** - Group similar partners together

### SEO
- Update "About" section regularly with relevant keywords
- Keep testimonials fresh and recent
- Partner associations boost credibility
- Social links improve engagement

---

## Troubleshooting

### "Only one site settings record can exist"
- You can only have ONE SiteSettings entry
- Edit the existing one instead of creating new ones

### Hero images not showing
- Check image file size (max 10MB)
- Ensure file format is JPG or PNG
- Verify image was successfully uploaded

### Social links not appearing
- Ensure "Is Active" is checked
- Verify correct URLs (should start with http:// or https://)
- Check ordering (lower numbers appear first)

### Changes not appearing on frontend
- Clear your browser cache (Ctrl+Shift+Delete)
- Wait a moment for caching to clear
- Check that "Is Active" is enabled for that item

---

## Support & Questions

For questions about:
- **Content management** - Check Admin Dashboard walkthrough above
- **Technical issues** - Contact your developer
- **Feature requests** - Add to development roadmap

---

## Version History

- **v1.0** (October 2025) - Initial dynamic content system launch
  - Hero slides with carousel
  - About section
  - Testimonials with ratings
  - Partners management
  - Site settings (contact info, hours)
  - Social media links


