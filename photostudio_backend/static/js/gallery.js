// Gallery Lightbox Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const modal = document.getElementById('imageModal');
    const lightboxModal = new bootstrap.Modal(modal);
    const lightboxImg = modal.querySelector('.lightbox-img');
    const lightboxTitle = modal.querySelector('.lightbox-title');
    const prevButton = modal.querySelector('.lightbox-prev');
    const nextButton = modal.querySelector('.lightbox-next');
    
    // Gallery items and current index
    let galleryItems = [];
    let currentIndex = 0;
    
    // Initialize gallery items based on visible tab
    function initGalleryItems() {
        const activeTab = document.querySelector('.tab-pane.active');
        if (!activeTab) return;
        
        galleryItems = Array.from(activeTab.querySelectorAll('.gallery-item'));
    }
    
    // Open lightbox with specific image
    function openLightbox(index) {
        if (index < 0 || index >= galleryItems.length) return;
        
        currentIndex = index;
        const item = galleryItems[currentIndex];
        const img = item.querySelector('img');
        
        // Update modal content
        lightboxImg.src = img.src;
        const category = item.querySelector('.badge') ? item.querySelector('.badge').textContent : '';
        lightboxTitle.textContent = category;
        
        lightboxModal.show();
    }
    
    // Navigate to previous image
    function prevImage() {
        currentIndex = (currentIndex - 1 + galleryItems.length) % galleryItems.length;
        const item = galleryItems[currentIndex];
        const img = item.querySelector('img');
        
        lightboxImg.src = img.src;
        const category = item.querySelector('.badge') ? item.querySelector('.badge').textContent : '';
        lightboxTitle.textContent = category;
    }
    
    // Navigate to next image
    function nextImage() {
        currentIndex = (currentIndex + 1) % galleryItems.length;
        const item = galleryItems[currentIndex];
        const img = item.querySelector('img');
        
        lightboxImg.src = img.src;
        const category = item.querySelector('.badge') ? item.querySelector('.badge').textContent : '';
        lightboxTitle.textContent = category;
    }
    
    // Listen for tab changes to update gallery items
    const tabButtons = document.querySelectorAll('[data-bs-toggle="pill"]');
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', initGalleryItems);
    });
    
    // Add click event to all gallery items
    document.addEventListener('click', function(e) {
        const galleryItem = e.target.closest('.gallery-item');
        if (!galleryItem) return;
        
        initGalleryItems();
        const index = galleryItems.indexOf(galleryItem);
        if (index !== -1) {
            openLightbox(index);
        }
    });
    
    // Navigation events
    prevButton.addEventListener('click', prevImage);
    nextButton.addEventListener('click', nextImage);
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (!modal.classList.contains('show')) return;
        
        if (e.key === 'ArrowLeft') {
            prevImage();
        } else if (e.key === 'ArrowRight') {
            nextImage();
        } else if (e.key === 'Escape') {
            lightboxModal.hide();
        }
    });
    
    // Swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    
    lightboxImg.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, false);
    
    lightboxImg.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);
    
    function handleSwipe() {
        const threshold = 50; // minimum distance for swipe
        
        if (touchEndX - touchStartX > threshold) {
            // Swipe right (prev)
            prevImage();
        } else if (touchStartX - touchEndX > threshold) {
            // Swipe left (next)
            nextImage();
        }
    }
    
    // Initialize gallery on page load
    initGalleryItems();
}); 