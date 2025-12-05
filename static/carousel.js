/**
 * Template Carousel/Slider Component
 * Features:
 * - Smooth animations with depth effect
 * - Mouse drag and touch support
 * - Keyboard navigation
 * - Responsive design
 */

class TemplateCarousel {
    constructor(containerSelector, options = {}) {
        this.container = document.querySelector(containerSelector);
        if (!this.container) return;

        this.track = this.container.querySelector('.carousel-track');
        this.slides = this.container.querySelectorAll('.template-slide');
        this.prevBtn = this.container.querySelector('.carousel-button.prev');
        this.nextBtn = this.container.querySelector('.carousel-button.next');

        this.currentIndex = 0;
        this.slideWidth = 290; // Default slide width
        this.gap = 40;
        this.isAnimating = false;
        this.isDragging = false;
        this.dragStartX = 0;
        this.dragCurrentX = 0;

        // Options
        this.autoPlay = options.autoPlay || false;
        this.autoPlayInterval = options.autoPlayInterval || 5000;
        this.autoPlayTimer = null;

        this.init();
    }

    init() {
        this.updateSlideWidth();
        this.updateCarousel();
        this.attachEventListeners();
        
        if (this.autoPlay) {
            this.startAutoPlay();
        }

        window.addEventListener('resize', () => {
            this.updateSlideWidth();
            this.updateCarousel();
        });
    }

    updateSlideWidth() {
        // Adjust slide width based on screen size
        const width = window.innerWidth;
        if (width < 480) {
            this.slideWidth = 150;
            this.gap = 15;
        } else if (width < 768) {
            this.slideWidth = 200;
            this.gap = 20;
        } else {
            this.slideWidth = 250;
            this.gap = 40;
        }
    }

    attachEventListeners() {
        // Button navigation
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });

        // Mouse drag
        this.track.addEventListener('mousedown', (e) => this.startDrag(e));
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', () => this.endDrag());

        // Touch support
        this.track.addEventListener('touchstart', (e) => this.startDrag(e));
        document.addEventListener('touchmove', (e) => this.drag(e));
        document.addEventListener('touchend', () => this.endDrag());

        // Click on slide to select
        this.slides.forEach((slide, index) => {
            slide.addEventListener('click', () => this.selectSlide(index));
        });
    }

    startDrag(e) {
        this.isDragging = true;
        this.dragStartX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
        this.dragCurrentX = this.dragStartX;
        
        if (this.autoPlay) {
            this.stopAutoPlay();
        }
    }

    drag(e) {
        if (!this.isDragging) return;

        this.dragCurrentX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
        const diff = this.dragCurrentX - this.dragStartX;

        // Apply subtle visual feedback while dragging
        this.track.style.transform = `translateX(calc(${-this.currentIndex * (this.slideWidth + this.gap)}px + ${diff}px))`;
    }

    endDrag() {
        if (!this.isDragging) return;
        this.isDragging = false;

        const diff = this.dragCurrentX - this.dragStartX;
        const threshold = 50;

        if (diff > threshold) {
            this.prev();
        } else if (diff < -threshold) {
            this.next();
        } else {
            this.updateCarousel();
        }

        if (this.autoPlay) {
            this.startAutoPlay();
        }
    }

    prev() {
        if (this.isAnimating) return;
        this.currentIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.updateCarousel();
    }

    next() {
        if (this.isAnimating) return;
        this.currentIndex = (this.currentIndex + 1) % this.slides.length;
        this.updateCarousel();
    }

    selectSlide(index) {
        if (this.isAnimating) return;
        this.currentIndex = index;
        this.updateCarousel();
    }

    updateCarousel() {
        this.isAnimating = true;

        // Calculate translation
        const offset = -this.currentIndex * (this.slideWidth + this.gap);
        
        // Smooth animation
        this.track.style.transition = 'transform 0.6s cubic-bezier(0.4, 0.0, 0.2, 1)';
        this.track.style.transform = `translateX(${offset}px)`;

        // Update slide states
        this.slides.forEach((slide, index) => {
            if (index === this.currentIndex) {
                slide.classList.add('center');
            } else {
                slide.classList.remove('center');
            }
        });

        setTimeout(() => {
            this.isAnimating = false;
        }, 600);
    }

    startAutoPlay() {
        this.autoPlayTimer = setInterval(() => this.next(), this.autoPlayInterval);
    }

    stopAutoPlay() {
        if (this.autoPlayTimer) {
            clearInterval(this.autoPlayTimer);
            this.autoPlayTimer = null;
        }
    }

    destroy() {
        this.stopAutoPlay();
        this.track.style.transition = 'none';
    }
}

// Template selection function
function selectTemplate(templateId, templateName) {
    // Store selected template in session/localStorage
    localStorage.setItem('selectedTemplate', templateId);
    localStorage.setItem('selectedTemplateName', templateName);
    
    // Redirect to card builder
    window.location.href = '/card/builder/';
}

// Initialize carousel when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const carousel = new TemplateCarousel('.templates-carousel', {
        autoPlay: false,
        autoPlayInterval: 5000
    });

    // Expose to global scope if needed
    window.templateCarousel = carousel;
});

