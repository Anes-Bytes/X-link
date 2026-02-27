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
function validateUsername(username) {
    // Basic username validation: 3-32 chars, alphanumeric and underscore
    const usernameRegex = /^[a-zA-Z0-9_]{3,32}$/;
    return usernameRegex.test(username);
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
        const usernameInput = loginForm.querySelector('input[name="username"]');
        const passwordInput = loginForm.querySelector('input[name="password"]');
        const username = usernameInput.value.trim();
        const password = passwordInput.value;

        clearErrors(loginForm);

        if (!username) {
            e.preventDefault();
            showError(loginForm, 'نام کاربری الزامی است');
            usernameInput.focus();
            return;
        }

        if (!password) {
            e.preventDefault();
            showError(loginForm, 'رمز عبور الزامی است');
            passwordInput.focus();
            return;
        }
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
        const usernameInput = signupForm.querySelector('input[name="username"]');
        const fullNameInput = signupForm.querySelector('input[name="full_name"]');
        const passwordInput = signupForm.querySelector('input[name="password"]');        
        const username = usernameInput.value.trim();
        const fullName = fullNameInput.value.trim();
        const password = passwordInput.value;
        clearErrors(signupForm);

        if (!username) {
            e.preventDefault();
            showError(signupForm, 'نام کاربری الزامی است');
            usernameInput.focus();
            return;
        }

        if (!validateUsername(username)) {
            e.preventDefault();
            showError(signupForm, 'نام کاربری باید ۳ تا ۳۲ کاراکتر و شامل حروف، اعداد یا زیرخط باشد');
            usernameInput.focus();
            return;
        }

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

        if (!password) {
            e.preventDefault();
            showError(signupForm, 'رمز عبور الزامی است');
            passwordInput.focus();
            return;
        }

        if (password.length < 8) {
            e.preventDefault();
            showError(signupForm, 'رمز عبور باید حداقل ۸ کاراکتر باشد');
            passwordInput.focus();
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

