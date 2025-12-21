// ============================================
// MOBILE NAVIGATION TOGGLE
// ============================================
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
}

// ============================================
// MESSAGES SYSTEM
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach((message, index) => {
        setTimeout(() => {
            hideMessage(message);
        }, 5000 + (index * 500)); // Stagger the hiding
    });

    // Close button functionality
    const closeButtons = document.querySelectorAll('.message-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.closest('.message');
            hideMessage(message);
        });
    });
});

function hideMessage(message) {
    if (!message) return;

    message.classList.add('fade-out');
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 300);
}

// ============================================
// HERO SLIDER
// ============================================
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const totalSlides = slides.length;

function showSlide(index) {
    // Remove active class from all slides and dots
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    // Add active class to current slide and dot
    if (slides[index]) {
        slides[index].classList.add('active');
    }
    if (dots[index]) {
        dots[index].classList.add('active');
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

// Auto-advance slider every 4 seconds
if (slides.length > 0) {
    setInterval(nextSlide, 4000);
}

// Dot navigation
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentSlide = index;
        showSlide(currentSlide);
    });
});

// ============================================
// SMOOTH SCROLL FOR NAVIGATION LINKS
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ============================================
// SCROLL-TRIGGERED ANIMATIONS (AOS)
// ============================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('aos-animate');
        }
    });
}, observerOptions);

// Observe all elements with data-aos attribute
document.querySelectorAll('[data-aos]').forEach(el => {
    observer.observe(el);
});

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.background = 'rgba(10, 15, 31, 0.95)';
        navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.background = 'rgba(10, 15, 31, 0.8)';
        navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
});

// ============================================
// PARALLAX EFFECT FOR HERO SECTION
// ============================================
const hero = document.querySelector('.hero');
const orbs = document.querySelectorAll('.gradient-orb');

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    if (hero && scrolled < window.innerHeight) {
        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 0.5;
            orb.style.transform = `translateY(${scrolled * speed}px)`;
        });
    }
});

// ============================================
// CTA BUTTON ANIMATION
// ============================================
const ctaButton = document.querySelector('.cta-button');
if (ctaButton) {
    ctaButton.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        this.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
}

// ============================================
// TEMPLATE CARDS HOVER EFFECT ENHANCEMENT
// ============================================
const templateCards = document.querySelectorAll('.template-card');
templateCards.forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
    });

    card.addEventListener('mouseleave', function() {
        card.style.transform = '';
    });
});

// ============================================
// PRICING CARDS INTERACTIVE EFFECT
// ============================================
const pricingCards = document.querySelectorAll('.pricing-card');
pricingCards.forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const glowX = (x - centerX) / centerX;
        const glowY = (y - centerY) / centerY;

        card.style.boxShadow = `
            ${glowX * 20}px ${glowY * 20}px 60px rgba(58, 134, 255, 0.3),
            0 0 40px rgba(58, 134, 255, 0.2)
        `;
    });

    card.addEventListener('mouseleave', function() {
        card.style.boxShadow = '';
    });
});

// ============================================
// BRAND SLIDER PAUSE ON HOVER
// ============================================
const brandSlider = document.getElementById('brandSlider');
if (brandSlider) {
    brandSlider.addEventListener('mouseenter', () => {
        brandSlider.style.animationPlayState = 'paused';
    });

    brandSlider.addEventListener('mouseleave', () => {
        brandSlider.style.animationPlayState = 'running';
    });
}

// ============================================
// SOCIAL ICONS HOVER EFFECT
// ============================================
const socialIcons = document.querySelectorAll('.social-icon');
socialIcons.forEach(icon => {
    icon.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px) scale(1.1)';
    });

    icon.addEventListener('mouseleave', function() {
        this.style.transform = '';
    });
});

// ============================================
// INITIALIZE ANIMATIONS ON LOAD
// ============================================
window.addEventListener('load', () => {
    // Fade in hero content
    const heroText = document.querySelector('.hero-text');
    if (heroText) {
        heroText.style.opacity = '0';
        heroText.style.animation = 'fadeInUp 1s ease-out forwards';
    }

    // Animate template cards on load
    const templateCards = document.querySelectorAll('.template-card');
    templateCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// ============================================
// CURSOR GLOW EFFECT (OPTIONAL ENHANCEMENT)
// ============================================
let cursorGlow = null;

document.addEventListener('mousemove', (e) => {
    if (!cursorGlow) {
        cursorGlow = document.createElement('div');
        cursorGlow.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(58, 134, 255, 0.3), transparent);
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease;
            mix-blend-mode: screen;
        `;
        document.body.appendChild(cursorGlow);
    }

    cursorGlow.style.left = e.clientX - 10 + 'px';
    cursorGlow.style.top = e.clientY - 10 + 'px';
});

// ============================================
// PERFORMANCE OPTIMIZATION: THROTTLE SCROLL EVENTS
// ============================================
function throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply throttle to scroll events
const throttledScroll = throttle(() => {
    // Scroll-based animations are handled here
}, 16); // ~60fps

window.addEventListener('scroll', throttledScroll);

// ============================================
// ADD RIPPLE EFFECT STYLES DYNAMICALLY
// ============================================
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

