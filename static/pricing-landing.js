/* ============================================
   PRICING SECTION - LANDING PAGE FUNCTIONALITY
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize pricing functionality
    initializePricingToggle();
    initializeFeatureAnimations();
});

/* ============================================
   BILLING TOGGLE FUNCTIONALITY
   ============================================ */

function initializePricingToggle() {
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    
    if (!toggleBtns.length) return;
    
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            toggleBtns.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get selected period
            const period = this.getAttribute('data-period');
            
            // Update prices based on period
            updatePrices(period);
            
            // Add animation
            animatePriceChange();
        });
    });
}

function updatePrices(period) {
    const cards = document.querySelectorAll('.pricing-card-landing');
    
    cards.forEach(card => {
        const priceElement = card.querySelector('.price-value');
        const periodElement = card.querySelector('.price-period');
        
        if (!priceElement) return;
        
        // Get original price from data attribute or calculate
        let monthlyPrice = parseFloat(priceElement.textContent.replace(/,/g, ''));
        let finalPrice = monthlyPrice;
        
        // Apply annual discount (25%)
        if (period === 'annual') {
            finalPrice = Math.round((monthlyPrice * 12) * 0.75);
            periodElement.textContent = '/سال';
        } else {
            periodElement.textContent = '/ماه';
        }
        
        // Update price with animation
        animatePriceUpdate(priceElement, finalPrice);
    });
}

function animatePriceUpdate(element, newPrice) {
    const currentPrice = parseFloat(element.textContent.replace(/,/g, ''));
    
    if (currentPrice === newPrice) return;
    
    element.style.opacity = '0.5';
    element.style.transform = 'scale(0.95)';
    
    setTimeout(() => {
        element.textContent = formatPrice(newPrice);
        element.style.opacity = '1';
        element.style.transform = 'scale(1)';
        element.style.transition = 'all 0.3s ease';
    }, 150);
}

function formatPrice(price) {
    return Math.round(price).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function animatePriceChange() {
    const cards = document.querySelectorAll('.pricing-card-landing');
    
    cards.forEach((card, index) => {
        card.style.animation = 'none';
        setTimeout(() => {
            card.style.animation = `slideUp 0.5s ease ${index * 0.1}s forwards`;
        }, 10);
    });
}

/* ============================================
   FEATURE ANIMATIONS
   ============================================ */

function initializeFeatureAnimations() {
    const cards = document.querySelectorAll('.pricing-card-landing');
    
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCard(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    cards.forEach(card => observer.observe(card));
}

function animateCard(card) {
    const features = card.querySelectorAll('.features-list-landing li');
    
    features.forEach((feature, index) => {
        feature.style.opacity = '0';
        feature.style.transform = 'translateX(-20px)';
        feature.style.animation = `slideInLeft 0.5s ease ${index * 0.1 + 0.3}s forwards`;
    });
}

/* ============================================
   SMOOTH SCROLL FOR COMPARISON TABLE
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    const comparisonBtn = document.querySelector('[href="#pricing-landing"]');
    
    if (comparisonBtn) {
        comparisonBtn.addEventListener('click', function(e) {
            const target = document.querySelector('.comparison-section-landing');
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
});

/* ============================================
   RESPONSIVE TABLE FUNCTIONALITY
   ============================================ */

function makeTableResponsive() {
    const tables = document.querySelectorAll('.comparison-table-landing table');
    
    tables.forEach(table => {
        if (window.innerWidth <= 768) {
            // Add data-label attributes for mobile view
            const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                cells.forEach((cell, index) => {
                    if (index > 0) { // Skip first column
                        cell.setAttribute('data-label', headers[index]);
                    }
                });
            });
        }
    });
}

// Initialize on load and on resize
makeTableResponsive();
window.addEventListener('resize', makeTableResponsive);

/* ============================================
   ADD CSS ANIMATIONS
   ============================================ */

const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Mobile table styles */
    @media (max-width: 768px) {
        .comparison-table-landing table td::before {
            content: attr(data-label);
            font-weight: 700;
            display: block;
            font-size: 12px;
            margin-bottom: 5px;
            color: var(--cyan-neon);
        }
    }
    
    /* Smooth transitions */
    .toggle-btn {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .pricing-card-landing {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .price-value {
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style);
