# Quick Reference - CSS Classes & HTML Structure

## Navbar Structure

### HTML
```html
<nav class="navbar">
    <div class="nav-container">
        <a href="/" class="logo-link">
            <div class="logo">
                <span class="logo-text">X-link</span>
            </div>
        </a>
        
        <div class="nav-user-section">
            <a href="/dashboard" class="nav-user-btn nav-btn-primary">
                Dashboard
            </a>
        </div>
        
        <div class="hamburger" id="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
        
        <ul class="nav-menu" id="navMenu">
            <li><a href="#" class="nav-link">Link</a></li>
            ...
        </ul>
    </div>
</nav>
```

### Key CSS Classes
- `.navbar` - Fixed navigation bar
- `.nav-container` - Flex container for alignment
- `.logo-link` - Clickable logo (links to home)
- `.nav-user-section` - Login/Dashboard button container (always visible)
- `.nav-user-btn` - User action button
- `.nav-user-btn.nav-btn` - Outlined button (not logged in)
- `.nav-user-btn.nav-btn-primary` - Gradient button (logged in)
- `.hamburger` - Three-line menu icon
- `.hamburger.active` - X-shaped icon state
- `.nav-menu` - Navigation links list
- `.nav-menu.active` - Expanded menu on mobile
- `.nav-link` - Individual navigation links

---

## Hero Section

### HTML
```html
<section class="hero">
    <div class="hero-background">
        <div class="gradient-orb orb-1"></div>
        <div class="gradient-orb orb-2"></div>
    </div>
    
    <div class="hero-content">
        <div class="hero-text">
            <h1 class="hero-title">
                <span class="title-line">Line 1</span>
                <span class="title-line">Line 2</span>
            </h1>
            <p class="hero-description">Description text</p>
            <a href="#" class="cta-button">
                <span>Text</span>
                <i class="fas fa-arrow-right"></i>
            </a>
        </div>
    </div>
    
    <div class="hero-slider">
        <div class="slider-container" id="heroSlider">
            <div class="slide active">
                <div class="slide-content">
                    <h3>Title</h3>
                    <p>Description</p>
                </div>
            </div>
            ...
        </div>
        <div class="slider-dots">
            <span class="dot active" data-slide="1"></span>
            ...
        </div>
    </div>
</section>
```

### Key CSS Classes
- `.hero` - Main hero container
- `.hero-background` - Background with animated orbs
- `.gradient-orb` - Animated background element
- `.hero-content` - Text content wrapper
- `.hero-title` - Main heading (uses clamp() for fluid scaling)
- `.title-line` - Individual heading lines
- `.hero-description` - Subtitle text
- `.cta-button` - Main call-to-action button
- `.slider-container` - Banner/slide container
- `.slide` - Individual slide
- `.slide.active` - Visible slide
- `.slider-dots` - Dot navigation
- `.dot` - Individual dot

---

## Customers Section

### HTML
```html
<section class="customers-section" id="customers">
    <div class="container">
        <h2 class="section-title">X-Link Customers</h2>
        <div class="brand-slider-container">
            <div class="brand-slider-track" id="brandSlider">
                <div class="brand-item">
                    <div class="brand-logo">
                        <img src="logo.png" alt="Company">
                    </div>
                </div>
                ...
            </div>
        </div>
    </div>
</section>
```

### Key CSS Classes
- `.customers-section` - Section wrapper
- `.section-title` - Section heading (gradient text)
- `.brand-slider-container` - Scroll container
- `.brand-slider-track` - Animated track (scrolls continuously)
- `.brand-item` - Individual brand item
- `.brand-logo` - Logo container
- `.brand-logo-text` - Text fallback for brands without logos
- `.brand-slider-track:hover` - Pauses animation

---

## Templates Section

### HTML
```html
<section class="templates-section" id="templates">
    <div class="container">
        <h2 class="section-title">Template Title</h2>
        
        <div class="templates-grid">
            <div class="template-card">
                <div class="template-image-wrapper">
                    <img src="template.jpg" alt="Template Name" class="template-image">
                </div>
                
                <div class="template-info">
                    <h3 class="template-name">Template Name</h3>
                    <a href="#" class="template-select-btn">
                        Button Text
                    </a>
                </div>
            </div>
            ...
        </div>
    </div>
</section>
```

### Key CSS Classes
- `.templates-section` - Section wrapper
- `.templates-grid` - Responsive grid layout
- `.template-card` - Individual template card
- `.template-card::before` - Top border animation
- `.template-card:hover` - Hover state
- `.template-image-wrapper` - Image container (16:12 aspect ratio)
- `.template-image` - Template image
- `.template-card:hover .template-image` - Zoom on hover
- `.template-info` - Card info section
- `.template-name` - Template title
- `.template-select-btn` - Action button
- `.no-templates` - Empty state message

---

## Footer Structure

### HTML
```html
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-brand">
                <h3 class="footer-logo">Logo</h3>
                <p class="footer-tagline">Tagline</p>
            </div>
            
            <div class="footer-section">
                <h4 class="footer-section-title">Section Title</h4>
                <ul class="footer-links">
                    <li><a href="#">Link</a></li>
                    ...
                </ul>
            </div>
            
            <div class="footer-section footer-team">
                <li>
                    <span class="team-role">Founder:</span>
                    <a href="#">@username</a>
                </li>
                ...
            </div>
            
            <div class="footer-section footer-social-section">
                <h4 class="footer-section-title">Social</h4>
                <div class="social-icons">
                    <a href="#" class="social-icon" aria-label="Instagram">
                        <i class="fab fa-instagram"></i>
                    </a>
                    ...
                </div>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>© 2025 Company</p>
            <p>Made with ❤️</p>
        </div>
    </div>
</footer>
```

### Key CSS Classes
- `.footer` - Footer wrapper
- `.footer-content` - Grid container for sections
- `.footer-brand` - Brand section (logo + tagline)
- `.footer-logo` - Logo text (gradient)
- `.footer-tagline` - Tagline text
- `.footer-section` - Individual section
- `.footer-section-title` - Section heading
- `.footer-links` - Links list
- `.footer-links a` - Links with hover effects
- `.footer-team` - Team section with larger gap
- `.team-role` - Role label (Founder/Co-founder)
- `.footer-social-section` - Social icons section
- `.social-icons` - Icons container
- `.social-icon` - Individual icon (44x44px)
- `.social-icon:hover` - Icon hover state
- `.enamad-badge` - Badge container
- `.footer-bottom` - Footer bottom copyright

---

## Responsive Breakpoints

### Desktop (> 1024px)
```css
/* Full featured layout */
.templates-grid { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }
.footer-content { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
```

### Tablet (768px - 1024px)
```css
/* Adjusted spacing and columns */
.templates-grid { grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }
.footer-content { grid-template-columns: repeat(2, 1fr); } /* 2 columns */
```

### Mobile (< 768px)
```css
/* Hamburger menu, optimized layout */
.nav-menu { position: fixed; left: -100%; } /* Hidden by default */
.nav-menu.active { left: 0; } /* Shown when active */
.hamburger { display: flex; } /* Show hamburger */
.footer-content { grid-template-columns: 1fr; } /* 1 column */
```

### Small Phone (< 480px)
```css
/* Minimal, touch-optimized */
.templates-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
.hero-title { font-size: clamp(26px, 7vw, 36px); }
```

---

## CSS Custom Properties (Variables)

```css
:root {
    --bg-dark: #0A0F1F;           /* Dark background */
    --primary-blue: #3A86FF;      /* Primary color */
    --cyan-neon: #00F6FF;         /* Accent color */
    --text-white: #F5F8FF;        /* Main text */
    --text-gray: rgba(245, 248, 255, 0.7); /* Secondary text */
}
```

---

## Animation Classes

### Available Animations
```css
@keyframes fadeInUp {
    /* Fade in and slide up */
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    /* Floating background orbs */
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(30px, -30px) scale(1.1); }
}

@keyframes scroll {
    /* Continuous scroll effect */
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
```

### Usage
```html
<!-- Fade in on scroll (requires JS observer) -->
<div data-aos="fade-up">Content</div>

<!-- Automatic animations -->
<button class="cta-button"><!-- Fades in on page load --></button>
<div class="brand-slider-track"><!-- Scrolls continuously --></div>
```

---

## Button States

### Default Button
```html
<a href="#" class="nav-user-btn nav-btn">Login</a>
```
- Border: 1.5px blue
- Background: Transparent
- On Hover: Light blue background

### Primary Button
```html
<a href="#" class="nav-user-btn nav-btn-primary">Dashboard</a>
```
- Background: Blue-to-Cyan gradient
- Text: Dark background
- On Hover: Lift up + shadow

### CTA Button
```html
<a href="#" class="cta-button">
    <span>Start Free</span>
    <i class="fas fa-arrow-right"></i>
</a>
```
- Background: Blue-to-Cyan gradient
- Icon animates on hover
- Shadow effect

### Template Button
```html
<a href="#" class="template-select-btn">Create Card</a>
```
- Gradient background
- Inline-block, auto margin-top
- Works responsively

---

## JavaScript Integration

### Hamburger Menu
```javascript
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close menu on link click
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});
```

### Hero Slider
```javascript
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

function showSlide(index) {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));
    
    slides[index]?.classList.add('active');
    dots[index]?.classList.add('active');
}

// Auto-advance every 4 seconds
setInterval(() => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}, 4000);

// Dot navigation
dots.forEach((dot, idx) => {
    dot.addEventListener('click', () => {
        currentSlide = idx;
        showSlide(currentSlide);
    });
});
```

---

## Common Modifications

### Change Primary Color
```css
:root {
    --primary-blue: #Your-Color;
    --cyan-neon: #Your-Accent;
}
```

### Adjust Button Size
```css
.nav-user-btn {
    padding: 12px 28px; /* Increase from 10px 24px */
    font-size: 16px;    /* Increase from 14px */
}
```

### Modify Grid Columns
```css
.templates-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    /* Change minmax(300px) to adjust column width */
}
```

### Change Animation Speed
```css
.template-card {
    transition: all 0.6s ease; /* Change from 0.4s */
}
```

---

## Accessibility Features

- ✅ Semantic HTML (`<nav>`, `<footer>`, `<section>`)
- ✅ ARIA labels on icons (`aria-label="Instagram"`)
- ✅ Alt text on images
- ✅ Proper link titles
- ✅ Focus states on interactive elements
- ✅ Sufficient color contrast
- ✅ Keyboard navigation support

---

## Performance Tips

1. **Images:** Use proper sizing, lazy loading where possible
2. **CSS:** Minify before deployment
3. **JavaScript:** Keep event listeners minimal
4. **Animations:** Use CSS animations (GPU accelerated)
5. **Font:** Use system fonts or limit custom fonts

---

**Last Updated:** December 15, 2025
**Version:** 1.0
**Status:** Production Ready
