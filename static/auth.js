// ============================================
// AUTH PAGE - TAB SWITCHING
// ============================================
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');

authTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.getAttribute('data-tab');
        
        // Remove active class from all tabs and forms
        authTabs.forEach(t => t.classList.remove('active'));
        authForms.forEach(f => f.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding form
        tab.classList.add('active');
        document.getElementById(`${targetTab}Form`).classList.add('active');
    });
});

// ============================================
// FORM VALIDATION
// ============================================
function validatePhoneNumber(phone) {
    // Iranian mobile number validation
    const phoneRegex = /^09\d{9}$/;
    return phoneRegex.test(phone);
}

function showError(form, message) {
    // Remove existing error messages
    const existingError = form.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }

    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.innerHTML = `
        <div class="error-content">
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
        </div>
    `;

    // Insert error message at the top of the form
    form.insertBefore(errorDiv, form.firstChild);
}

function clearErrors(form) {
    const error = form.querySelector('.form-error');
    if (error) {
        error.remove();
    }
}

// ============================================
// FORM SUBMISSION HANDLERS
// ============================================
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');

if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        const phoneInput = loginForm.querySelector('input[name="phone"]');
        const phone = phoneInput.value.trim();

        clearErrors(loginForm);

        if (!phone) {
            e.preventDefault();
            showError(loginForm, 'شماره تلفن الزامی است');
            phoneInput.focus();
            return;
        }

        if (!validatePhoneNumber(phone)) {
            e.preventDefault();
            showError(loginForm, 'شماره تلفن باید با ۰۹ شروع شود و ۱۱ رقم باشد');
            phoneInput.focus();
            return;
        }
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
        const phoneInput = signupForm.querySelector('input[name="phone"]');
        const fullNameInput = signupForm.querySelector('input[name="full_name"]');
        const phone = phoneInput.value.trim();
        const fullName = fullNameInput.value.trim();

        clearErrors(signupForm);

        if (!fullName) {
            e.preventDefault();
            showError(signupForm, 'نام کامل الزامی است');
            fullNameInput.focus();
            return;
        }

        if (fullName.length < 2) {
            e.preventDefault();
            showError(signupForm, 'نام کامل باید حداقل ۲ حرف باشد');
            fullNameInput.focus();
            return;
        }

        if (!phone) {
            e.preventDefault();
            showError(signupForm, 'شماره تلفن الزامی است');
            phoneInput.focus();
            return;
        }

        if (!validatePhoneNumber(phone)) {
            e.preventDefault();
            showError(signupForm, 'شماره تلفن باید با ۰۹ شروع شود و ۱۱ رقم باشد');
            phoneInput.focus();
            return;
        }
    });
}

// ============================================
// SOCIAL LOGIN BUTTONS
// ============================================
const socialButtons = document.querySelectorAll('.social-btn');

socialButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        const provider = button.classList.contains('google-btn') ? 'Google' : 'GitHub';
        console.log(`Continue with ${provider}`);
        // Handle social login logic here
    });
});

