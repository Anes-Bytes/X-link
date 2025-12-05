// ============================================
// CARD TEMPLATE INTERACTIVITY
// ============================================

// Initialize card animations on load
window.addEventListener('load', () => {
    const card = document.getElementById('businessCard');
    if (card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px) scale(0.95)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.8s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
        }, 100);
    }

    // Animate sections sequentially
    const sections = document.querySelectorAll('.card-section');
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            section.style.transition = 'all 0.6s ease-out';
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, 300 + (index * 100));
    });
});

// ============================================
// CONTACT BUTTON INTERACTIONS
// ============================================
const contactButtons = document.querySelectorAll('.contact-btn');

contactButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        `;

        this.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add ripple animation style
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// SOCIAL LINK HOVER EFFECTS
// ============================================
const socialLinks = document.querySelectorAll('.social-link');

socialLinks.forEach(link => {
    link.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px) scale(1.1)';
    });

    link.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ============================================
// SKILL PILL ANIMATIONS
// ============================================
const skillPills = document.querySelectorAll('.skill-pill');

skillPills.forEach((pill, index) => {
    pill.style.opacity = '0';
    pill.style.transform = 'scale(0.8)';
    
    setTimeout(() => {
        pill.style.transition = 'all 0.3s ease';
        pill.style.opacity = '1';
        pill.style.transform = 'scale(1)';
    }, 800 + (index * 50));
});

// ============================================
// PORTFOLIO ITEM INTERACTIONS
// ============================================
const portfolioItems = document.querySelectorAll('.portfolio-item');

portfolioItems.forEach(item => {
    const thumbnail = item.querySelector('.portfolio-thumbnail');
    
    thumbnail.addEventListener('mouseenter', function() {
        const img = this.querySelector('img');
        if (img) {
            img.style.transform = 'scale(1.1)';
        }
    });
    
    thumbnail.addEventListener('mouseleave', function() {
        const img = this.querySelector('img');
        if (img) {
            img.style.transform = 'scale(1)';
        }
    });
});

// ============================================
// PARALLAX EFFECT ON SCROLL
// ============================================
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const card = document.getElementById('businessCard');
    
    if (card && scrolled < window.innerHeight) {
        const parallaxSpeed = 0.3;
        card.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
    }
    
    lastScroll = scrolled;
});

// ============================================
// CARD GLOW EFFECT ON MOUSE MOVE
// ============================================
const businessCard = document.getElementById('businessCard');

if (businessCard) {
    businessCard.addEventListener('mousemove', (e) => {
        const rect = businessCard.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const glowX = (x - centerX) / centerX;
        const glowY = (y - centerY) / centerY;
        
        businessCard.style.boxShadow = `
            ${glowX * 20}px ${glowY * 20}px 60px rgba(58, 134, 255, 0.3),
            0 0 40px rgba(58, 134, 255, 0.2)
        `;
    });
    
    businessCard.addEventListener('mouseleave', () => {
        businessCard.style.boxShadow = '0 20px 60px rgba(0, 0, 0, 0.3)';
    });
}

// ============================================
// DATA POPULATION FUNCTION
// ============================================
// This function can be used to dynamically populate card data
function populateCardData(data) {
    if (data.fullName) {
        const fullNameEl = document.getElementById('fullName');
        if (fullNameEl) fullNameEl.textContent = data.fullName;
    }
    
    if (data.jobTitle) {
        const jobTitleEl = document.getElementById('jobTitle');
        if (jobTitleEl) jobTitleEl.textContent = data.jobTitle;
    }
    
    if (data.shortBio) {
        const shortBioEl = document.getElementById('shortBio');
        if (shortBioEl) shortBioEl.textContent = data.shortBio;
    }
    
    if (data.phone) {
        const phoneBtn = document.getElementById('phoneBtn');
        const phoneText = document.getElementById('phoneText');
        if (phoneBtn) phoneBtn.href = `tel:${data.phone}`;
        if (phoneText) phoneText.textContent = data.phone;
    }
    
    if (data.email) {
        const emailBtn = document.getElementById('emailBtn');
        const emailText = document.getElementById('emailText');
        if (emailBtn) emailBtn.href = `mailto:${data.email}`;
        if (emailText) emailText.textContent = data.email;
    }
    
    if (data.website) {
        const websiteBtn = document.getElementById('websiteBtn');
        const websiteText = document.getElementById('websiteText');
        if (websiteBtn) websiteBtn.href = data.website;
        if (websiteText) websiteText.textContent = data.website.replace(/^https?:\/\//, '');
    }
    
    if (data.profileImage) {
        const profileImg = document.getElementById('profileImg');
        if (profileImg) profileImg.src = data.profileImage;
    }
    
    // Update social links
    if (data.socialLinks) {
        Object.keys(data.socialLinks).forEach(platform => {
            const link = document.querySelector(`.social-link[data-platform="${platform}"]`);
            if (link && data.socialLinks[platform]) {
                link.href = data.socialLinks[platform];
            }
        });
    }
    
    // Update skills
    if (data.skills && Array.isArray(data.skills)) {
        const skillsContainer = document.getElementById('skillsContainer');
        if (skillsContainer) {
            skillsContainer.innerHTML = '';
            data.skills.forEach(skill => {
                const pill = document.createElement('span');
                pill.className = 'skill-pill';
                pill.textContent = skill;
                skillsContainer.appendChild(pill);
            });
        }
    }
    
    // Update services
    if (data.services && Array.isArray(data.services)) {
        const servicesContainer = document.getElementById('servicesContainer');
        if (servicesContainer) {
            servicesContainer.innerHTML = '';
            data.services.forEach(service => {
                const item = document.createElement('div');
                item.className = 'service-item';
                item.innerHTML = `
                    <i class="${service.icon || 'fas fa-check'}"></i>
                    <span>${service.name}</span>
                `;
                servicesContainer.appendChild(item);
            });
        }
    }
    
    // Update portfolio
    if (data.portfolio && Array.isArray(data.portfolio)) {
        const portfolioGrid = document.getElementById('portfolioGrid');
        if (portfolioGrid) {
            portfolioGrid.innerHTML = '';
            data.portfolio.forEach(item => {
                const portfolioItem = document.createElement('div');
                portfolioItem.className = 'portfolio-item';
                portfolioItem.innerHTML = `
                    <div class="portfolio-thumbnail">
                        <img src="${item.image}" alt="${item.title}">
                        <div class="portfolio-overlay">
                            <a href="${item.link}" class="portfolio-link" target="_blank">
                                <i class="fas fa-external-link-alt"></i>
                            </a>
                        </div>
                    </div>
                    <p class="portfolio-title">${item.title}</p>
                `;
                portfolioGrid.appendChild(portfolioItem);
            });
        }
    }
}

// Example usage (commented out):
// populateCardData({
//     fullName: 'Jane Smith',
//     jobTitle: 'Creative Director',
//     shortBio: 'Passionate about design and innovation.',
//     phone: '+1 (555) 123-4567',
//     email: 'jane@example.com',
//     website: 'https://janesmith.com',
//     profileImage: 'https://example.com/profile.jpg',
//     socialLinks: {
//         instagram: 'https://instagram.com/jane',
//         linkedin: 'https://linkedin.com/in/jane',
//         github: 'https://github.com/jane'
//     },
//     skills: ['Design', 'Branding', 'UI/UX'],
//     services: [
//         { name: 'Branding', icon: 'fas fa-palette' },
//         { name: 'Web Design', icon: 'fas fa-laptop-code' }
//     ],
//     portfolio: [
//         { title: 'Project 1', image: 'https://example.com/img1.jpg', link: 'https://example.com/project1' }
//     ]
// });

