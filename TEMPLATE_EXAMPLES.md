# Template Examples - Dynamic Content Integration

This file shows example HTML snippets for integrating dynamic content into your home page template.

## 1. Hero Section (Carousel)

```html
<!-- Hero Section - Rotating Banner Carousel -->
<section id="hero" class="hero-section">
    {% if hero_slides %}
        <div class="hero-carousel" id="heroCarousel">
            {% for slide in hero_slides %}
                <div class="hero-slide {% if forloop.first %}active{% endif %}">
                    <!-- Hero Image Background -->
                    <img src="{{ slide.image.url }}" alt="{{ slide.title }}" class="hero-image">
                    
                    <!-- Overlay -->
                    <div class="hero-overlay"></div>
                    
                    <!-- Content -->
                    <div class="hero-content container">
                        <h1 class="hero-title">{{ slide.title }}</h1>
                        {% if slide.subtitle %}
                            <p class="hero-subtitle">{{ slide.subtitle }}</p>
                        {% endif %}
                        {% if slide.description %}
                            <p class="hero-description">{{ slide.description }}</p>
                        {% endif %}
                        
                        <!-- CTA Button -->
                        {% if slide.cta_text and slide.cta_url %}
                            <a href="{{ slide.cta_url }}" class="btn btn-primary hero-cta">
                                {{ slide.cta_text }}
                            </a>
                        {% endif %}
                    </div>
                </div>
            {% endfor %}
        </div>
        
        <!-- Carousel Controls (if multiple slides) -->
        {% if hero_slides.count > 1 %}
            <button class="carousel-control prev" onclick="prevSlide()">❮</button>
            <button class="carousel-control next" onclick="nextSlide()">❯</button>
            <div class="carousel-indicators">
                {% for slide in hero_slides %}
                    <span class="indicator {% if forloop.first %}active{% endif %}"></span>
                {% endfor %}
            </div>
        {% endif %}
    {% endif %}
</section>

<style>
.hero-section {
    position: relative;
    height: 500px;
    overflow: hidden;
}

.hero-carousel {
    position: relative;
    width: 100%;
    height: 100%;
}

.hero-slide {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.hero-slide.active {
    opacity: 1;
}

.hero-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
}

.hero-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
    z-index: 10;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 20px;
    text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
}

.carousel-control {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.3);
    border: none;
    color: white;
    font-size: 2rem;
    padding: 15px 20px;
    cursor: pointer;
    z-index: 20;
    transition: background 0.3s;
}

.carousel-control:hover {
    background: rgba(255, 255, 255, 0.5);
}

.carousel-control.prev {
    left: 20px;
}

.carousel-control.next {
    right: 20px;
}

.carousel-indicators {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
    display: flex;
    gap: 10px;
}

.indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: background 0.3s;
}

.indicator.active {
    background: white;
}
</style>
```

---

## 2. About Section

```html
<!-- About Section -->
<section id="about" class="about-section py-5">
    {% if about_section %}
        <div class="container">
            <div class="row align-items-center">
                <!-- Image -->
                <div class="col-lg-6 mb-4 mb-lg-0">
                    <img src="{{ about_section.image.url }}" 
                         alt="{{ about_section.name }}" 
                         class="img-fluid rounded about-image">
                </div>
                
                <!-- Content -->
                <div class="col-lg-6">
                    <h2 class="section-title">Hello, I'm {{ about_section.name }}</h2>
                    <p class="subtitle text-muted">{{ about_section.title }}</p>
                    
                    <!-- Description -->
                    <div class="about-description">
                        {{ about_section.description|linebreaks }}
                    </div>
                    
                    <!-- Extended Bio -->
                    {% if about_section.bio %}
                        <div class="about-bio mt-3">
                            {{ about_section.bio|linebreaks }}
                        </div>
                    {% endif %}
                    
                    <!-- CTA Button -->
                    {% if about_section.cta_text and about_section.cta_url %}
                        <a href="{{ about_section.cta_url }}" class="btn btn-primary mt-4">
                            {{ about_section.cta_text }} →
                        </a>
                    {% endif %}
                </div>
            </div>
        </div>
    {% endif %}
</section>

<style>
.about-section {
    background: #f8f9fa;
}

.section-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #002b4d;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 1.1rem;
    margin-bottom: 20px;
}

.about-image {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.about-description {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #555;
}

.about-description p {
    margin-bottom: 15px;
}
</style>
```

---

## 3. Testimonials Section

```html
<!-- Testimonials Section -->
<section id="testimonials" class="testimonials-section py-5">
    {% if testimonials %}
        <div class="container">
            <h2 class="section-title text-center mb-5">
                Read what my clients have to say about their experience
            </h2>
            
            <div class="testimonials-carousel" id="testimonialsCarousel">
                {% for testimonial in testimonials %}
                    <div class="testimonial-card {% if forloop.first %}active{% endif %}">
                        <!-- Testimonial Text -->
                        <div class="testimonial-text">
                            <p class="quote-mark">"</p>
                            <p class="testimonial-content">
                                {{ testimonial.testimonial_text }}
                            </p>
                        </div>
                        
                        <!-- Client Info -->
                        <div class="testimonial-footer">
                            {% if testimonial.client_image %}
                                <img src="{{ testimonial.client_image.url }}" 
                                     alt="{{ testimonial.client_name }}" 
                                     class="client-avatar">
                            {% endif %}
                            
                            <div class="client-info">
                                <p class="client-name">{{ testimonial.client_name }}</p>
                                <p class="client-type text-muted">
                                    {{ testimonial.client_type }}
                                </p>
                                
                                <!-- Star Rating -->
                                <div class="rating">
                                    {% for star in testimonial|rjust:testimonial.rating %}
                                        ⭐
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
            
            <!-- Carousel Controls -->
            {% if testimonials.count > 1 %}
                <div class="text-center mt-4">
                    <button class="carousel-btn" onclick="prevTestimonial()">❮</button>
                    <button class="carousel-btn" onclick="nextTestimonial()">❯</button>
                </div>
                
                <div class="carousel-indicators mt-3">
                    {% for testimonial in testimonials %}
                        <span class="indicator {% if forloop.first %}active{% endif %}"></span>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    {% endif %}
</section>

<style>
.testimonials-section {
    background: #1a3a52;
    color: white;
}

.testimonials-carousel {
    position: relative;
    min-height: 300px;
}

.testimonial-card {
    position: absolute;
    width: 100%;
    opacity: 0;
    transition: opacity 0.5s;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

.testimonial-card.active {
    opacity: 1;
    position: relative;
}

.quote-mark {
    font-size: 3rem;
    opacity: 0.3;
    margin-bottom: 0;
}

.testimonial-content {
    font-size: 1.1rem;
    font-style: italic;
    line-height: 1.8;
    margin: 20px 0;
}

.testimonial-footer {
    display: flex;
    align-items: center;
    margin-top: 20px;
}

.client-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-right: 15px;
    object-fit: cover;
}

.client-name {
    margin: 0;
    font-weight: bold;
}

.client-type {
    margin: 5px 0;
    font-size: 0.9rem;
}

.rating {
    margin-top: 5px;
}
</style>
```

---

## 4. Partners Section

```html
<!-- Partners & Collaborations Section -->
<section id="partners" class="partners-section py-5">
    {% if partners %}
        <div class="container">
            <h2 class="section-title text-center mb-5">
                Partners & Collaborations
            </h2>
            <p class="text-center mb-5 text-muted">
                Working with amazing brands and organizations to create exceptional content
            </p>
            
            <div class="partners-carousel" id="partnersCarousel">
                {% regroup partners by category as partners_by_category %}
                
                {% for category in partners_by_category %}
                    <div class="partners-group">
                        {% for partner in category.list %}
                            <div class="partner-card">
                                {% if partner.website_url %}
                                    <a href="{{ partner.website_url }}" 
                                       target="_blank" 
                                       title="{{ partner.name }}">
                                        <img src="{{ partner.logo.url }}" 
                                             alt="{{ partner.name }}" 
                                             class="partner-logo">
                                    </a>
                                {% else %}
                                    <img src="{{ partner.logo.url }}" 
                                         alt="{{ partner.name }}" 
                                         class="partner-logo">
                                {% endif %}
                                <p class="partner-name">{{ partner.name }}</p>
                                {% if partner.description %}
                                    <p class="partner-category">{{ partner.description }}</p>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                {% endfor %}
            </div>
            
            <!-- Carousel Controls -->
            {% if partners.count > 3 %}
                <div class="text-center mt-4">
                    <button class="carousel-btn" onclick="prevPartner()">❮</button>
                    <button class="carousel-btn" onclick="nextPartner()">❯</button>
                </div>
            {% endif %}
        </div>
    {% endif %}
</section>

<style>
.partners-section {
    background: #f8f9fa;
}

.partner-card {
    background: white;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s, box-shadow 0.3s;
    height: 100%;
}

.partner-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.partner-logo {
    max-width: 150px;
    max-height: 80px;
    object-fit: contain;
    margin-bottom: 15px;
}

.partner-name {
    font-weight: bold;
    margin: 15px 0 5px 0;
}

.partner-category {
    color: #666;
    font-size: 0.9rem;
    margin: 0;
}

.partners-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
}
</style>
```

---

## 5. Contact Information Section

```html
<!-- Contact Section -->
<section id="contact" class="contact-section py-5">
    {% if site_settings %}
        <div class="container">
            <div class="row">
                <!-- Contact Info -->
                <div class="col-md-6">
                    <h3 class="section-title mb-4">Get In Touch</h3>
                    
                    <div class="contact-item">
                        <h5>📧 Email</h5>
                        <p><a href="mailto:{{ site_settings.email }}">
                            {{ site_settings.email }}
                        </a></p>
                    </div>
                    
                    <div class="contact-item">
                        <h5>📞 Phone</h5>
                        <p><a href="tel:{{ site_settings.phone }}">
                            {{ site_settings.phone }}
                        </a></p>
                    </div>
                    
                    <div class="contact-item">
                        <h5>📍 Studio Address</h5>
                        <p>{{ site_settings.get_full_address }}</p>
                    </div>
                    
                    <div class="contact-item">
                        <h5>⏰ Business Hours</h5>
                        <p>
                            <strong>Monday - Friday:</strong> 
                            {{ site_settings.monday_friday_open|time:"g:i A" }} - 
                            {{ site_settings.monday_friday_close|time:"g:i A" }}<br>
                            <strong>Saturday:</strong> 
                            {{ site_settings.saturday_open|time:"g:i A" }} - 
                            {{ site_settings.saturday_close|time:"g:i A" }}
                        </p>
                    </div>
                </div>
                
                <!-- Contact Form -->
                <div class="col-md-6">
                    <h3 class="section-title mb-4">Send a Message</h3>
                    <form class="contact-form">
                        <div class="form-group mb-3">
                            <input type="text" class="form-control" 
                                   placeholder="Your Name" required>
                        </div>
                        <div class="form-group mb-3">
                            <input type="email" class="form-control" 
                                   placeholder="Your Email" required>
                        </div>
                        <div class="form-group mb-3">
                            <textarea class="form-control" rows="5" 
                                      placeholder="Your Message"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                </div>
            </div>
        </div>
    {% endif %}
</section>

<style>
.contact-item {
    margin-bottom: 25px;
}

.contact-item h5 {
    font-weight: bold;
    margin-bottom: 8px;
}

.contact-item a {
    color: #002b4d;
    text-decoration: none;
}

.contact-form input,
.contact-form textarea {
    border: 1px solid #ddd;
    border-radius: 4px;
}
</style>
```

---

## 6. Footer with Social Links

```html
<!-- Footer -->
<footer class="footer bg-dark text-white py-5">
    <div class="container">
        <div class="row mb-4">
            <!-- Logo & Tagline -->
            <div class="col-md-3 mb-4">
                <h5>SHOTZ</h5>
                {% if site_settings.tagline %}
                    <p class="text-muted">{{ site_settings.tagline }}</p>
                {% endif %}
                
                <!-- Social Media Links -->
                {% if social_links %}
                    <div class="social-links mt-3">
                        {% for link in social_links %}
                            <a href="{{ link.url }}" 
                               target="_blank" 
                               title="{{ link.get_platform_display }}"
                               class="social-icon">
                                {% if link.platform == 'instagram' %}
                                    📷
                                {% elif link.platform == 'facebook' %}
                                    👥
                                {% elif link.platform == 'twitter' %}
                                    🐦
                                {% elif link.platform == 'youtube' %}
                                    📺
                                {% elif link.platform == 'linkedin' %}
                                    💼
                                {% elif link.platform == 'tiktok' %}
                                    🎵
                                {% elif link.platform == 'pinterest' %}
                                    📌
                                {% else %}
                                    🔗
                                {% endif %}
                            </a>
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <!-- Quick Links -->
            <div class="col-md-3 mb-4">
                <h5>Quick Links</h5>
                <ul class="list-unstyled">
                    <li><a href="{% url 'home' %}" class="text-muted">Home</a></li>
                    <li><a href="{% url 'about' %}" class="text-muted">About</a></li>
                    <li><a href="{% url 'services' %}" class="text-muted">Services</a></li>
                    <li><a href="{% url 'gallery' %}" class="text-muted">Gallery</a></li>
                </ul>
            </div>
            
            <!-- Services -->
            <div class="col-md-3 mb-4">
                <h5>Services</h5>
                <ul class="list-unstyled">
                    {% for service in active_services|slice:":4" %}
                        <li><a href="{{ service.get_absolute_url }}" 
                               class="text-muted">
                            {{ service.title }}
                        </a></li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- Contact Info -->
            <div class="col-md-3 mb-4">
                {% if site_settings %}
                    <h5>Contact</h5>
                    <p class="text-muted">
                        📍 {{ site_settings.address_line1 }}<br>
                        {{ site_settings.city }}, {{ site_settings.state }}<br>
                        📞 {{ site_settings.phone }}<br>
                        📧 {{ site_settings.email }}
                    </p>
                {% endif %}
            </div>
        </div>
        
        <!-- Copyright -->
        <hr class="bg-secondary">
        <div class="row">
            <div class="col-md-6">
                <p class="text-muted mb-0">
                    © 2025 SHOTZ. All rights reserved.
                </p>
            </div>
            <div class="col-md-6 text-end">
                <a href="#" class="text-muted me-3">Privacy Policy</a>
                <a href="#" class="text-muted">Terms of Service</a>
            </div>
        </div>
    </div>
</footer>

<style>
.social-links {
    display: flex;
    gap: 15px;
}

.social-icon {
    font-size: 1.5rem;
    opacity: 0.7;
    transition: opacity 0.3s;
}

.social-icon:hover {
    opacity: 1;
}

footer a {
    text-decoration: none;
}

footer a:hover {
    color: white !important;
}
</style>
```

---

## JavaScript for Carousel Functions

```javascript
<script>
let currentHeroSlide = 0;
let currentTestimonialSlide = 0;
let currentPartnerSlide = 0;

// Hero Carousel
function showHeroSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.carousel-indicators .indicator');
    
    if (index >= slides.length) currentHeroSlide = 0;
    if (index < 0) currentHeroSlide = slides.length - 1;
    
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    slides[currentHeroSlide].classList.add('active');
    indicators[currentHeroSlide].classList.add('active');
}

function nextSlide() {
    currentHeroSlide++;
    showHeroSlide(currentHeroSlide);
}

function prevSlide() {
    currentHeroSlide--;
    showHeroSlide(currentHeroSlide);
}

// Testimonials Carousel
function showTestimonialSlide(index) {
    const slides = document.querySelectorAll('.testimonial-card');
    if (index >= slides.length) currentTestimonialSlide = 0;
    if (index < 0) currentTestimonialSlide = slides.length - 1;
    
    slides.forEach(slide => slide.classList.remove('active'));
    slides[currentTestimonialSlide].classList.add('active');
}

function nextTestimonial() {
    currentTestimonialSlide++;
    showTestimonialSlide(currentTestimonialSlide);
}

function prevTestimonial() {
    currentTestimonialSlide--;
    showTestimonialSlide(currentTestimonialSlide);
}

// Auto-rotate carousels every 5 seconds
setInterval(() => {
    nextSlide();
}, 5000);

setInterval(() => {
    nextTestimonial();
}, 5000);

// Initialize
showHeroSlide(currentHeroSlide);
showTestimonialSlide(currentTestimonialSlide);
</script>
```

---

## Notes

- All sections pull data dynamically from the database
- Images are served from MEDIA_URL
- Add your own CSS to match your site's design
- Star ratings can be displayed using Django template filter or JavaScript
- Carousel auto-rotates every 5 seconds
- Responsive classes from Bootstrap are used (col-lg-6, col-md-6, etc.)
- All sections are optional (check for existence before rendering)
- Social links display with emoji icons (can replace with Font Awesome)


