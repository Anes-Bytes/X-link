/* ============================================
   FAILED PAGE - JAVASCRIPT
   ============================================ */

// Parse query parameters
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadFailedDetails();
    setupPaymentOptions();
});

// ============================================
// LOAD FAILED DETAILS
// ============================================

function loadFailedDetails() {
    const plan = getQueryParam('plan') || 'Professional';
    const price = getQueryParam('price') || '29';

    // Update plan name
    document.getElementById('planName').textContent = capitalizeFirst(plan);

    // Update amount
    document.getElementById('amount').textContent = `$${price}.00/month`;

    // Set attempt time
    document.getElementById('attemptTime').textContent = 'Just now';

    // Store in localStorage
    const failedData = {
        plan: plan,
        price: price,
        timestamp: new Date().toISOString(),
        attempts: (parseInt(localStorage.getItem('paymentAttempts') || '0') + 1)
    };
    localStorage.setItem('paymentAttempts', failedData.attempts.toString());
    localStorage.setItem('failedData', JSON.stringify(failedData));

    // Show different error messages based on attempt count
    showErrorMessage(failedData.attempts);
}

// ============================================
// ERROR MESSAGES
// ============================================

function showErrorMessage(attempts) {
    const messages = [
        'Your card was declined. Please check your card details.',
        'Transaction failed. Insufficient funds in your account.',
        'Security check failed. Contact your bank.',
        'Network error occurred. Please try again.',
        'Maximum retry limit reached. Contact support.'
    ];

    const messageIndex = Math.min(attempts - 1, messages.length - 1);
    document.getElementById('errorMessage').textContent = messages[messageIndex];
}

// ============================================
// RETRY PAYMENT
// ============================================

function retryPayment() {
    const failedData = JSON.parse(localStorage.getItem('failedData') || '{}');

    // Show loading state
    const retryBtn = document.querySelector('.btn-primary');
    const originalContent = retryBtn.innerHTML;
    retryBtn.disabled = true;
    retryBtn.innerHTML = '<span>Processing...</span> <i class="fas fa-spinner fa-spin"></i>';

    // Simulate retry processing
    setTimeout(() => {
        // 70% chance of success on retry
        const isSuccess = Math.random() < 0.7;

        if (isSuccess) {
            redirectToSuccess(failedData.plan, failedData.price);
        } else {
            // Reset button
            retryBtn.disabled = false;
            retryBtn.innerHTML = originalContent;

            // Show error notification
            showNotification('Payment still failed. Try another payment method or contact support.', 'error');

            // Increment attempts
            const attempts = parseInt(localStorage.getItem('paymentAttempts') || '0') + 1;
            localStorage.setItem('paymentAttempts', attempts.toString());
            showErrorMessage(attempts);
        }
    }, 2500);
}

// ============================================
// CONTACT SUPPORT
// ============================================

function contactSupport() {
    // Open support modal or page
    const supportModal = document.createElement('div');
    supportModal.className = 'support-modal';
    supportModal.innerHTML = `
        <div class="support-modal-content">
            <button class="modal-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>

            <h2>Contact Support</h2>
            <p>Our team is here to help you resolve your payment issue.</p>

            <div class="support-methods">
                <div class="support-method">
                    <i class="fas fa-envelope"></i>
                    <h4>Email Support</h4>
                    <p>support@x-link.com</p>
                    <p style="font-size: 0.8rem; color: rgba(245, 248, 255, 0.5);">Response time: 2-4 hours</p>
                </div>

                <div class="support-method">
                    <i class="fas fa-phone"></i>
                    <h4>Phone Support</h4>
                    <p>+1 (555) 123-4567</p>
                    <p style="font-size: 0.8rem; color: rgba(245, 248, 255, 0.5);">Available: 9 AM - 6 PM EST</p>
                </div>

                <div class="support-method">
                    <i class="fas fa-comments"></i>
                    <h4>Live Chat</h4>
                    <p>Chat with us now</p>
                    <p style="font-size: 0.8rem; color: rgba(245, 248, 255, 0.5);">Available: 24/7</p>
                </div>
            </div>

            <div class="support-form">
                <h4>Or send us a message</h4>
                <form onsubmit="sendSupportMessage(event)">
                    <input type="email" placeholder="Your email" required>
                    <textarea placeholder="Describe your issue..." rows="4" required></textarea>
                    <button type="submit" class="submit-btn">
                        <span>Send Message</span>
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>
    `;

    document.body.appendChild(supportModal);
    supportModal.style.animation = 'modalSlideIn 0.4s ease-out';
}

// ============================================
// SEND SUPPORT MESSAGE
// ============================================

function sendSupportMessage(event) {
    event.preventDefault();

    const submitBtn = event.target.querySelector('.submit-btn');
    const originalContent = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Sending...</span> <i class="fas fa-spinner fa-spin"></i>';

    // Simulate sending
    setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalContent;

        // Close modal and show success
        document.querySelector('.support-modal').remove();
        showNotification('Support message sent! We\'ll get back to you soon.', 'success');
    }, 1500);
}

// ============================================
// SELECT PAYMENT METHOD
// ============================================

function selectPaymentMethod(method) {
    const failedData = JSON.parse(localStorage.getItem('failedData') || '{}');

    showNotification(`Redirecting to ${method.replace('-', ' ')} payment...`, 'info');

    setTimeout(() => {
        // In a real app, redirect to the appropriate payment processor
        if (method === 'paypal') {
            window.location.href = 'https://www.paypal.com';
        } else if (method === 'bank-transfer') {
            showBankTransferInfo(failedData.price);
        } else {
            // Retry with credit card
            retryPayment();
        }
    }, 1000);
}

// ============================================
// BANK TRANSFER INFO
// ============================================

function showBankTransferInfo(amount) {
    const bankModal = document.createElement('div');
    bankModal.className = 'bank-modal';
    bankModal.innerHTML = `
        <div class="bank-modal-content">
            <button class="modal-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>

            <h2>Bank Transfer Details</h2>
            <p>Transfer the amount to the following account:</p>

            <div class="bank-details">
                <div class="detail">
                    <span class="label">Account Holder:</span>
                    <span class="value">X-Link Inc.</span>
                </div>
                <div class="detail">
                    <span class="label">Account Number:</span>
                    <span class="value" onclick="copyToClipboard('1234567890')">1234567890 <i class="fas fa-copy"></i></span>
                </div>
                <div class="detail">
                    <span class="label">Routing Number:</span>
                    <span class="value" onclick="copyToClipboard('021000021')">021000021 <i class="fas fa-copy"></i></span>
                </div>
                <div class="detail">
                    <span class="label">Bank Name:</span>
                    <span class="value">Global Bank Corp.</span>
                </div>
                <div class="detail">
                    <span class="label">Amount:</span>
                    <span class="value">$${amount}.00</span>
                </div>
            </div>

            <p style="margin-top: 1.5rem; color: rgba(245, 248, 255, 0.6); font-size: 0.9rem;">
                Please allow 3-5 business days for the transfer to be processed.
            </p>
        </div>
    `;

    document.body.appendChild(bankModal);
    bankModal.style.animation = 'modalSlideIn 0.4s ease-out';
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    });
}

function redirectToSuccess(plan, price) {
    const params = new URLSearchParams({
        plan: plan,
        price: price,
        period: 'monthly'
    });
    window.location.href = `payment-success.html?${params.toString()}`;
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    // Auto remove
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.4s ease-out forwards';
        setTimeout(() => notification.remove(), 400);
    }, 4000);
}

// ============================================
// SETUP PAYMENT OPTIONS
// ============================================

function setupPaymentOptions() {
    const paymentOptions = document.querySelectorAll('.payment-option');
    paymentOptions.forEach((option, index) => {
        option.style.animation = `fadeInUp 0.6s ease-out ${1.0 + index * 0.1}s both`;
    });
}

// ============================================
// ADD STYLES PROGRAMMATICALLY
// ============================================

const styles = document.createElement('style');
styles.textContent = `
    .support-modal,
    .bank-modal {
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

    .support-modal-content,
    .bank-modal-content {
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
        right: 1.5rem;
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

    .support-modal-content h2,
    .bank-modal-content h2 {
        color: #F5F8FF;
        margin-bottom: 1rem;
    }

    .support-modal-content > p,
    .bank-modal-content > p {
        color: rgba(245, 248, 255, 0.7);
        margin-bottom: 1.5rem;
    }

    .support-methods {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .support-method {
        background: rgba(0, 246, 255, 0.05);
        border: 1px solid rgba(0, 246, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }

    .support-method i {
        font-size: 2rem;
        color: #00F6FF;
        margin-bottom: 0.75rem;
        display: block;
    }

    .support-method h4 {
        color: #F5F8FF;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .support-method p {
        color: rgba(245, 248, 255, 0.7);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }

    .support-form {
        margin-top: 2rem;
    }

    .support-form h4 {
        color: #F5F8FF;
        margin-bottom: 1rem;
    }

    .support-form input,
    .support-form textarea {
        width: 100%;
        padding: 0.75rem 1rem;
        background: rgba(58, 134, 255, 0.05);
        border: 1px solid rgba(0, 246, 255, 0.2);
        border-radius: 8px;
        color: #F5F8FF;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }

    .support-form input::placeholder,
    .support-form textarea::placeholder {
        color: rgba(245, 248, 255, 0.3);
    }

    .support-form input:focus,
    .support-form textarea:focus {
        outline: none;
        background: rgba(58, 134, 255, 0.1);
        border-color: #00F6FF;
        box-shadow: 0 0 20px rgba(0, 246, 255, 0.2);
    }

    .submit-btn {
        width: 100%;
        padding: 0.75rem;
        background: linear-gradient(135deg, #3A86FF, #00F6FF);
        color: #0A0F1F;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        transition: all 0.3s ease;
    }

    .submit-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 246, 255, 0.3);
    }

    .submit-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .bank-details {
        background: rgba(0, 246, 255, 0.05);
        border: 1px solid rgba(0, 246, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
    }

    .bank-details .detail {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(0, 246, 255, 0.05);
    }

    .bank-details .detail:last-child {
        border-bottom: none;
    }

    .bank-details .label {
        color: rgba(245, 248, 255, 0.6);
        font-size: 0.9rem;
    }

    .bank-details .value {
        color: #F5F8FF;
        font-weight: 600;
        font-family: 'Courier New', monospace;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .bank-details .value:hover {
        color: #00F6FF;
    }

    .bank-details .value i {
        margin-left: 0.5rem;
        font-size: 0.8rem;
    }

    .notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #3A86FF, #00F6FF);
        color: #0A0F1F;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideIn 0.4s ease-out;
    }

    .notification-error {
        background: linear-gradient(135deg, #FF4757, #FFA502);
    }

    .notification-success {
        background: linear-gradient(135deg, #2ED573, #00F6FF);
    }

    .notification-info {
        background: linear-gradient(135deg, #3A86FF, #00F6FF);
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

    @keyframes slideIn {
        from {
            transform: translateX(400px);
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
            transform: translateX(400px);
            opacity: 0;
        }
    }

    @media (max-width: 480px) {
        .support-modal-content,
        .bank-modal-content {
            padding: 1.5rem;
        }

        .support-methods {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(styles);
