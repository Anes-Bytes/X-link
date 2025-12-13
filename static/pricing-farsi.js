/* ============================================
   PRICING PAGE - JAVASCRIPT - FARSI VERSION
   ============================================ */

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initBillingToggle();
    initFAQ();
    initAnimations();
});

// ============================================
// BILLING TOGGLE FUNCTIONALITY
// ============================================

function initBillingToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            
            const period = button.dataset.period;
            updatePrices(period);
        });
    });
}

function updatePrices(period) {
    const pricingCards = document.querySelectorAll('.pricing-card');
    
    pricingCards.forEach(card => {
        const priceMonthly = card.querySelector('.price-monthly');
        const priceAnnual = card.querySelector('.price-annual');
        const periodLabel = card.querySelector('.period');
        
        if (period === 'annual') {
            priceMonthly.classList.add('hidden');
            priceAnnual.classList.remove('hidden');
            periodLabel.textContent = '/سال';
            
            // Animate price change
            priceAnnual.style.animation = 'none';
            setTimeout(() => {
                priceAnnual.style.animation = 'priceFlip 0.6s ease-out';
            }, 10);
        } else {
            priceAnnual.classList.add('hidden');
            priceMonthly.classList.remove('hidden');
            periodLabel.textContent = '/ماه';
            
            // Animate price change
            priceMonthly.style.animation = 'none';
            setTimeout(() => {
                priceMonthly.style.animation = 'priceFlip 0.6s ease-out';
            }, 10);
        }
    });
}

// ============================================
// FAQ ACCORDION
// ============================================

function initFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const faqItem = question.parentElement;
            const faqAnswer = question.nextElementSibling;
            
            // Close other open FAQs
            document.querySelectorAll('.faq-item.open').forEach(item => {
                if (item !== faqItem) {
                    item.classList.remove('open');
                    item.querySelector('.faq-answer').classList.add('hidden');
                }
            });
            
            // Toggle current FAQ
            faqItem.classList.toggle('open');
            faqAnswer.classList.toggle('hidden');
        });
    });
}

// ============================================
// PLAN SELECTION
// ============================================

function selectPlan(plan, price) {
    // Get billing period
    const activeToggle = document.querySelector('.toggle-btn.active');
    const period = activeToggle.dataset.period;
    
    // Store plan details
    const planDetails = {
        plan: plan,
        price: price,
        period: period,
        timestamp: new Date().toISOString()
    };
    
    // Save to localStorage
    localStorage.setItem('selectedPlan', JSON.stringify(planDetails));
    
    // Show confirmation or redirect to payment
    showPaymentFlow(plan, price, period);
}

// ============================================
// PAYMENT FLOW
// ============================================

function showPaymentFlow(plan, price, period) {
    // Create payment modal
    const modal = document.createElement('div');
    modal.className = 'payment-modal';
    modal.innerHTML = `
        <div class="payment-modal-content">
            <button class="modal-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
            
            <div class="payment-header">
                <h3>تایید اشتراک</h3>
                <p>شما در حال ارتقا به پلان <strong>${getPlanNameFarsi(plan)}</strong> هستید</p>
            </div>
            
            <div class="payment-summary">
                <div class="summary-item">
                    <span>پلان</span>
                    <span>${getPlanNameFarsi(plan)}</span>
                </div>
                <div class="summary-item">
                    <span>قیمت</span>
                    <span>$${price}/${period === 'annual' ? 'سال' : 'ماه'}</span>
                </div>
                <div class="summary-item">
                    <span>دوره صورت‌حساب</span>
                    <span>${period === 'annual' ? 'سالانه' : 'ماهانه'}</span>
                </div>
            </div>
            
            <form class="payment-form">
                <div class="form-group">
                    <label>نام صاحب کارت</label>
                    <input type="text" placeholder="علی احمدی" required>
                </div>
                
                <div class="form-group">
                    <label>شماره کارت</label>
                    <input type="text" placeholder="1234 5678 9012 3456" maxlength="19" required>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>تاریخ انقضا</label>
                        <input type="text" placeholder="MM/YY" maxlength="5" required>
                    </div>
                    <div class="form-group">
                        <label>CVV</label>
                        <input type="text" placeholder="123" maxlength="3" required>
                    </div>
                </div>
                
                <button type="button" class="payment-btn" onclick="processPayment(this, '${plan}', ${price}, '${period}')">
                    <span>تکمیل پرداخت</span>
                    <i class="fas fa-lock"></i>
                </button>
            </form>
            
            <p class="payment-disclaimer">
                پرداخت شما امن و رمزگذاری شده است. ما هرگز جزئیات کارت خود را ذخیره نمی‌کنیم.
            </p>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.animation = 'modalSlideIn 0.4s ease-out';
    
    // Add keyboard support
    modal.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') modal.remove();
    });
}

function getPlanNameFarsi(plan) {
    const names = {
        'starter': 'شروعی',
        'professional': 'حرفه‌ای',
        'enterprise': 'سازمانی'
    };
    return names[plan] || plan;
}

function processPayment(button, plan, price, period) {
    // Disable button
    button.disabled = true;
    button.innerHTML = '<span>در حال پردازش...</span> <i class="fas fa-spinner fa-spin"></i>';
    
    // Simulate payment processing
    setTimeout(() => {
        // 80% chance of success
        const isSuccess = Math.random() < 0.8;
        
        // Remove modal
        document.querySelector('.payment-modal').remove();
        
        // Redirect to success or failed page
        if (isSuccess) {
            redirectToSuccess(plan, price, period);
        } else {
            redirectToFailed(plan, price);
        }
    }, 2000);
}

function redirectToSuccess(plan, price, period) {
    const params = new URLSearchParams({
        plan: plan,
        price: price,
        period: period
    });
    window.location.href = `payment-success-farsi.html?${params.toString()}`;
}

function redirectToFailed(plan, price) {
    const params = new URLSearchParams({
        plan: plan,
        price: price
    });
    window.location.href = `payment-failed-farsi.html?${params.toString()}`;
}

// ============================================
// ANIMATION ON SCROLL
// ============================================

function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.pricing-card, .comparison-section, .faq-section').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// ============================================
// CARD NUMBER FORMATTING
// ============================================

document.addEventListener('input', (e) => {
    if (e.target.placeholder === '1234 5678 9012 3456') {
        let value = e.target.value.replace(/\s/g, '');
        let formattedValue = value.replace(/(\d{4})/g, '$1 ').trim();
        e.target.value = formattedValue;
    }
    
    if (e.target.placeholder === 'MM/YY') {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
            value = value.slice(0, 2) + '/' + value.slice(2, 4);
        }
        e.target.value = value;
    }
    
    if (e.target.placeholder === '123') {
        e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3);
    }
});

// Add CSS animations programmatically
const styles = document.createElement('style');
styles.textContent = `
    @keyframes priceFlip {
        0% {
            transform: rotateY(90deg);
            opacity: 0;
        }
        50% {
            opacity: 0.5;
        }
        100% {
            transform: rotateY(0);
            opacity: 1;
        }
    }
    
    @keyframes modalSlideIn {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .payment-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 15, 31, 0.95);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        padding: 20px;
    }
    
    .payment-modal-content {
        background: linear-gradient(135deg, rgba(58, 134, 255, 0.05), rgba(0, 246, 255, 0.02));
        border: 1px solid rgba(0, 246, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        width: 100%;
        position: relative;
    }
    
    .modal-close {
        position: absolute;
        top: 1.5rem;
        left: 1.5rem;
        background: none;
        border: none;
        color: #F5F8FF;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .modal-close:hover {
        color: #00F6FF;
        transform: rotate(90deg);
    }
    
    .payment-header {
        margin-bottom: 2rem;
    }
    
    .payment-header h3 {
        font-size: 1.5rem;
        color: #F5F8FF;
        margin-bottom: 0.5rem;
    }
    
    .payment-header p {
        color: rgba(245, 248, 255, 0.7);
    }
    
    .payment-summary {
        background: rgba(0, 246, 255, 0.05);
        border: 1px solid rgba(0, 246, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(0, 246, 255, 0.05);
        color: rgba(245, 248, 255, 0.7);
    }
    
    .summary-item:last-child {
        border-bottom: none;
    }
    
    .payment-form {
        margin-bottom: 1.5rem;
    }
    
    .form-group {
        margin-bottom: 1.25rem;
    }
    
    .form-group label {
        display: block;
        color: #F5F8FF;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .form-group input {
        width: 100%;
        padding: 0.75rem 1rem;
        background: rgba(58, 134, 255, 0.05);
        border: 1px solid rgba(0, 246, 255, 0.2);
        border-radius: 8px;
        color: #F5F8FF;
        font-size: 1rem;
        transition: all 0.3s ease;
        font-family: 'Vazirmatn', sans-serif;
    }
    
    .form-group input::placeholder {
        color: rgba(245, 248, 255, 0.3);
    }
    
    .form-group input:focus {
        outline: none;
        background: rgba(58, 134, 255, 0.1);
        border-color: #00F6FF;
        box-shadow: 0 0 20px rgba(0, 246, 255, 0.2);
    }
    
    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    .payment-btn {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #3A86FF, #00F6FF);
        color: #0A0F1F;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
        font-size: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        transition: all 0.3s ease;
        font-family: 'Vazirmatn', sans-serif;
    }
    
    .payment-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 246, 255, 0.3);
    }
    
    .payment-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
    .payment-disclaimer {
        text-align: center;
        color: rgba(245, 248, 255, 0.5);
        font-size: 0.85rem;
    }
    
    @media (max-width: 480px) {
        .payment-modal-content {
            padding: 1.5rem;
        }
        
        .form-row {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(styles);
