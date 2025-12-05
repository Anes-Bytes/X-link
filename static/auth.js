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
// FORM SUBMISSION HANDLERS
// ============================================
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');

if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Handle login logic here
        console.log('Login form submitted');
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        // Handle signup logic here
        console.log('Signup form submitted');
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

