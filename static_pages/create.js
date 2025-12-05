// ============================================
// MULTI-STEP FORM NAVIGATION
// ============================================
let currentStep = 1;
const totalSteps = 3;

const stepIndicators = document.querySelectorAll('.step-indicator');
const formSteps = document.querySelectorAll('.form-step');
const stepLines = document.querySelectorAll('.step-line');

function updateStep(step) {
    // Update step indicators
    stepIndicators.forEach((indicator, index) => {
        const stepNum = index + 1;
        indicator.classList.remove('active', 'completed');
        
        if (stepNum < step) {
            indicator.classList.add('completed');
        } else if (stepNum === step) {
            indicator.classList.add('active');
        }
    });
    
    // Update step lines
    stepLines.forEach((line, index) => {
        if (index + 1 < step) {
            line.classList.add('completed');
        } else {
            line.classList.remove('completed');
        }
    });
    
    // Update form steps
    formSteps.forEach((formStep, index) => {
        formStep.classList.remove('active');
        if (index + 1 === step) {
            formStep.classList.add('active');
        }
    });
    
    currentStep = step;
}

// Next button handlers
document.querySelectorAll('.next-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const nextStep = parseInt(btn.getAttribute('data-next'));
        if (nextStep <= totalSteps) {
            updateStep(nextStep);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});

// Back button handlers
document.querySelectorAll('.back-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const prevStep = parseInt(btn.getAttribute('data-prev'));
        if (prevStep >= 1) {
            updateStep(prevStep);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});

// ============================================
// CHARACTER COUNT FOR BIO
// ============================================
const shortBio = document.getElementById('shortBio');
const bioCount = document.getElementById('bioCount');

if (shortBio && bioCount) {
    shortBio.addEventListener('input', () => {
        const count = shortBio.value.length;
        bioCount.textContent = count;
        
        if (count > 100) {
            bioCount.style.color = 'var(--cyan-neon)';
        } else {
            bioCount.style.color = 'var(--text-gray)';
        }
    });
}

// ============================================
// FILE UPLOAD HANDLING
// ============================================
const fileInput = document.getElementById('profilePhoto');
const fileUploadArea = document.getElementById('fileUploadArea');
const uploadContent = fileUploadArea.querySelector('.upload-content');
const uploadPreview = document.getElementById('uploadPreview');
const previewImage = document.getElementById('previewImage');
const removeImageBtn = document.getElementById('removeImage');

if (fileInput && fileUploadArea) {
    // Click to upload
    fileUploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = 'var(--primary-blue)';
        fileUploadArea.style.background = 'rgba(58, 134, 255, 0.1)';
    });
    
    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.style.borderColor = 'rgba(58, 134, 255, 0.3)';
        fileUploadArea.style.background = 'transparent';
    });
    
    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = 'rgba(58, 134, 255, 0.3)';
        fileUploadArea.style.background = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
}

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        alert('File size must be less than 5MB');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadContent.style.display = 'none';
        uploadPreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Remove image
if (removeImageBtn) {
    removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.value = '';
        previewImage.src = '';
        uploadContent.style.display = 'flex';
        uploadPreview.style.display = 'none';
    });
}

// ============================================
// LIVE USERNAME PREVIEW
// ============================================
const usernameInput = document.getElementById('username');
const linkUsername = document.getElementById('linkUsername');

if (usernameInput && linkUsername) {
    usernameInput.addEventListener('input', () => {
        let username = usernameInput.value.trim().toLowerCase();
        
        // Remove invalid characters (only allow letters, numbers, underscore, hyphen)
        username = username.replace(/[^a-z0-9_-]/g, '');
        
        // Update input value if it was cleaned
        if (username !== usernameInput.value.trim().toLowerCase()) {
            usernameInput.value = username;
        }
        
        // Update preview
        if (username) {
            linkUsername.textContent = username;
        } else {
            linkUsername.textContent = 'username';
        }
    });
    
    // Validate on blur
    usernameInput.addEventListener('blur', () => {
        let username = usernameInput.value.trim().toLowerCase();
        username = username.replace(/[^a-z0-9_-]/g, '');
        
        if (username.length < 3) {
            usernameInput.setCustomValidity('Username must be at least 3 characters');
        } else if (username.length > 30) {
            usernameInput.setCustomValidity('Username must be less than 30 characters');
        } else {
            usernameInput.setCustomValidity('');
        }
    });
}

// ============================================
// FORM SUBMISSION
// ============================================
const createForms = document.querySelectorAll('.create-form');

createForms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Collect all form data
        const formData = {
            fullName: document.getElementById('fullName')?.value || '',
            jobTitle: document.getElementById('jobTitle')?.value || '',
            shortBio: document.getElementById('shortBio')?.value || '',
            phone: document.getElementById('phone')?.value || '',
            email: document.getElementById('email')?.value || '',
            website: document.getElementById('website')?.value || '',
            instagram: document.getElementById('instagram')?.value || '',
            telegram: document.getElementById('telegram')?.value || '',
            linkedin: document.getElementById('linkedin')?.value || '',
            github: document.getElementById('github')?.value || '',
            twitter: document.getElementById('twitter')?.value || '',
            whatsapp: document.getElementById('whatsapp')?.value || '',
            youtube: document.getElementById('youtube')?.value || '',
            username: document.getElementById('username')?.value || '',
            profilePhoto: fileInput?.files[0] || null
        };
        
        console.log('Form submitted:', formData);
        
        // Here you would typically send the data to a server
        // For now, just show a success message
        alert('Your X-Link has been created successfully!');
    });
});

// ============================================
// INITIALIZE ON LOAD
// ============================================
window.addEventListener('load', () => {
    updateStep(1);
});




