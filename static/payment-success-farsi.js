/* ============================================
   SUCCESS PAGE - JAVASCRIPT - FARSI VERSION
   ============================================ */

// Parse query parameters
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadPlanDetails();
    startConfetti();
    setupFeatures();
});

// ============================================
// LOAD PLAN DETAILS
// ============================================

function loadPlanDetails() {
    const plan = getQueryParam('plan') || 'professional';
    const price = getQueryParam('price') || '29';
    const period = getQueryParam('period') || 'monthly';

    // Update plan name
    document.getElementById('planName').textContent = getPlanNameFarsi(plan);

    // Update amount paid
    const symbol = '$';
    const periodText = period === 'annual' ? '/سال' : '/ماه';
    document.getElementById('amountPaid').textContent = `${symbol}${price}.00${periodText}`;

    // Update billing cycle
    document.getElementById('billingCycle').textContent = period === 'annual' ? 'سالانه' : 'ماهانه';

    // Generate order ID
    const orderId = `ORD-${formatDate()}-${Math.floor(Math.random() * 100000).toString().padStart(5, '0')}`;
    document.getElementById('orderId').textContent = orderId;

    // Set transaction date - Persian date
    document.getElementById('transactionDate').textContent = getPersianDate(new Date());

    // Update features based on plan
    updateFeaturesForPlan(plan);

    // Store in localStorage
    const successData = {
        plan: plan,
        price: price,
        period: period,
        orderId: orderId,
        timestamp: new Date().toISOString()
    };
    localStorage.setItem('successData', JSON.stringify(successData));
}

// ============================================
// GET PLAN NAME IN FARSI
// ============================================

function getPlanNameFarsi(plan) {
    const names = {
        'starter': 'شروعی',
        'professional': 'حرفه‌ای',
        'enterprise': 'سازمانی'
    };
    return names[plan.toLowerCase()] || plan;
}

// ============================================
// GET PERSIAN DATE
// ============================================

function getPersianDate(date) {
    const months = ['ژانویه', 'فوریه', 'مارس', 'آپریل', 'مه', 'ژوئن', 
                    'ژوئیه', 'آگوست', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر'];
    const persianNumbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    
    const day = String(date.getDate()).split('').map(d => persianNumbers[d]).join('');
    const month = months[date.getMonth()];
    const year = String(date.getFullYear()).split('').map(d => persianNumbers[d]).join('');
    
    return `${day} ${month} ${year}`;
}

// ============================================
// UPDATE FEATURES BASED ON PLAN
// ============================================

function updateFeaturesForPlan(plan) {
    const featuresMap = {
        starter: [
            'تا ۵ کارت دیجیتال',
            'تجزیه‌وتحلیل پایه',
            'پشتیبانی از طریق ایمیل',
            'دسترسی به برنامه موبایل'
        ],
        professional: [
            'کارت‌های دیجیتال نامحدود',
            'تجزیه‌وتحلیل پیشرفته',
            'پشتیبانی اولویت‌دار',
            'دامنه‌های سفارشی (۵)',
            'همکاری تیمی',
            'دسترسی API'
        ],
        enterprise: [
            'همه‌چیز در پلان حرفه‌ای',
            'دامنه‌های سفارشی نامحدود',
            'مدیر حساب اختصاصی',
            'دسترسی کامل API',
            'حل نرم‌افزار سفید',
            'پشتیبانی ۲۴/۷ حرفه‌ای'
        ]
    };

    const features = featuresMap[plan.toLowerCase()] || featuresMap.professional;
    const featuresGrid = document.getElementById('featuresGrid');

    featuresGrid.innerHTML = features.map(feature => `
        <li>
            <i class="fas fa-check-circle"></i>
            <span>${feature}</span>
        </li>
    `).join('');
}

// ============================================
// CONFETTI ANIMATION
// ============================================

function startConfetti() {
    const canvas = document.getElementById('confettiCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const particleCount = 100;

    // Create particles
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            size: Math.random() * 4 + 2,
            speedX: (Math.random() - 0.5) * 8,
            speedY: Math.random() * 5 + 3,
            opacity: Math.random() * 0.5 + 0.5,
            color: getRandomColor(),
            rotation: Math.random() * Math.PI * 2,
            rotationSpeed: (Math.random() - 0.5) * 0.2
        });
    }

    function getRandomColor() {
        const colors = ['#2ED573', '#00F6FF', '#3A86FF', '#FFB800', '#FF6B6B'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((particle, index) => {
            particle.y += particle.speedY;
            particle.x += particle.speedX;
            particle.speedY += 0.1; // gravity
            particle.opacity -= 0.01;
            particle.rotation += particle.rotationSpeed;

            // Draw particle
            ctx.save();
            ctx.globalAlpha = particle.opacity;
            ctx.fillStyle = particle.color;
            ctx.translate(particle.x, particle.y);
            ctx.rotate(particle.rotation);
            ctx.fillRect(-particle.size / 2, -particle.size / 2, particle.size, particle.size);
            ctx.restore();

            // Remove if out of bounds
            if (particle.y > canvas.height || particle.opacity <= 0) {
                particles.splice(index, 1);
            }
        });

        if (particles.length > 0) {
            requestAnimationFrame(animate);
        }
    }

    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// ============================================
// SETUP FEATURES ANIMATION
// ============================================

function setupFeatures() {
    const features = document.querySelectorAll('.features-grid li');
    features.forEach((feature, index) => {
        feature.style.animation = `fadeInUp 0.6s ease-out ${0.9 + index * 0.1}s both`;
    });
}

// ============================================
// DOWNLOAD INVOICE
// ============================================

function downloadInvoice() {
    const successData = JSON.parse(localStorage.getItem('successData') || '{}');
    
    // Create a simple invoice content in Persian
    const invoiceContent = `
صورت‌حساب
========================================

شناسه سفارش: ${successData.orderId}
تاریخ: ${getPersianDate(new Date(successData.timestamp))}

پلان: ${getPlanNameFarsi(successData.plan)}
مبلغ: $${successData.price}.00
دوره صورت‌حساب: ${successData.period === 'annual' ? 'سالانه' : 'ماهانه'}

========================================
از اشتراک شما سپاسگزاریم!
به X-Link Pro خوش‌آمدید!

این صورت‌حساب برای سوابق شما صادر شده است.
برای پشتیبانی با ما تماس بگیرید: support@x-link.com
========================================
    `;

    // Create blob and download
    const blob = new Blob([invoiceContent], { type: 'text/plain; charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `invoice-${successData.orderId}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    // Show notification
    showNotification('صورت‌حساب دانلود شد!');
}

// ============================================
// NOTIFICATION
// ============================================

function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #2ED573, #00F6FF);
        color: #0A0F1F;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.4s ease-out;
        font-family: 'Vazirmatn', sans-serif;
    `;

    document.body.appendChild(notification);

    // Auto remove
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.4s ease-out forwards';
        setTimeout(() => notification.remove(), 400);
    }, 3000);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate() {
    const date = new Date();
    return `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
}

// ============================================
// ADD ANIMATIONS TO STYLESHEET
// ============================================

const styles = document.createElement('style');
styles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(-400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(-400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(styles);
