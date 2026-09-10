# Shotz — Feature Spec: Blog + Team Members

Agreed scope, implementation plan and conventions.

---

## 1. Blog (Event Stories / Coverage)

### URL structure
| URL | Purpose |
|-----|---------|
| `/blog/` | Listing of all published posts |
| `/blog/<slug>/` | Article / event story detail page |

### Home page
The current "Featured Work" photo grid is **replaced** by a Blog Cards section
showing the most recent 6 posts with `show_on_home=True`.

### Card design (home + listing)
- Full cover image
- Arrow (→) icon pinned to **top-right** of the card (always visible)
- Post title shown at the bottom — on **hover**: title color changes to accent orange, image scales slightly, overlay darkens
- Click anywhere on card → article page

### Article (detail) page layout
1. **Hero** — full-width cover image + title + date overlay
2. **Article body** — rich text (CKEditor)
3. **Event gallery** — cover_photo grid using existing GLightbox; shows album photos first, then any extra individually picked photos
4. **CTA strip** — "Book a session" → `/contact/`
5. **More stories** — 3 other recent posts at the bottom

### Model: `BlogPost`
| Field | Type | Notes |
|-------|------|-------|
| `title` | CharField(255) | |
| `slug` | SlugField(unique) | auto from title |
| `excerpt` | TextField | Short teaser (shown on card) |
| `body` | RichTextField | CKEditor — article content |
| `cover_image` | ImageField | Card + hero image |
| `album` | FK → Album (null, blank) | Main event gallery |
| `extra_photos` | M2M → Photo (blank) | Extra picks not in album |
| `meta_title` | CharField(160, blank) | SEO |
| `meta_description` | TextField(blank) | SEO |
| `published` | BooleanField(default=False) | Draft / live toggle |
| `show_on_home` | BooleanField(default=True) | Show in home cards |
| `published_at` | DateTimeField(null, blank) | Manual publish date |
| `created_at` | DateTimeField(auto_now_add) | |
| `updated_at` | DateTimeField(auto_now) | |

### Rich text dependency
```
uv add django-ckeditor
```
Add `'ckeditor'` to `INSTALLED_APPS` in `settings.py`.

### Migrations (run manually after code is applied)
```
python manage.py makemigrations
python manage.py migrate
```

---

## 2. Team Members

### Where it appears
- **About page** — after the "Why Choose Us" section, before the Journey timeline
- Model managed in Django Admin (Jazzmin)

### Model: `TeamMember`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField(255) | |
| `role` | CharField(255) | e.g. Lead Photographer |
| `photo` | ImageField | Portrait |
| `bio` | TextField(blank) | Short paragraph |
| `instagram` | URLField(blank) | |
| `linkedin` | URLField(blank) | |
| `twitter` | URLField(blank) | |
| `facebook` | URLField(blank) | |
| `order` | IntegerField(default=0) | Display order |
| `is_active` | BooleanField(default=True) | Show/hide |

### Migrations (run manually)
```
python manage.py makemigrations
python manage.py migrate
```

---

## 3. What is NOT changing
- Existing Gallery, Services, Albums, Photos, Videos models — untouched
- Admin theme (Jazzmin) — unchanged
- Featured Photos (`is_featured`) — still used, but no longer shown on home grid (blog cards replace that section)
- Contact form, testimonials, partners — untouched

---

## 4. Dependency checklist (run before migrations)
```bash
uv add django-ckeditor
```
Then add to `INSTALLED_APPS` (already handled in `settings.py` edit).
