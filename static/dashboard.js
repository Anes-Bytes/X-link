/* ============================================
   DASHBOARD - JAVASCRIPT FUNCTIONALITY
   ============================================ */

// DOM Elements
const sidebar = document.querySelector('.sidebar');
const mobileOverlay = document.getElementById('mobileOverlay');
const menuToggle = document.getElementById('menuToggle');

console.log('Dashboard JS loaded');
console.log('menuToggle element:', menuToggle);
console.log('sidebar element:', sidebar);
console.log('mobileOverlay element:', mobileOverlay);

// Check if elements exist and add event listeners safely
if (menuToggle) {
    console.log('Adding click listener to menuToggle');
    menuToggle.addEventListener('click', () => {
        console.log('Menu toggle clicked');
        if (sidebar) {
            sidebar.classList.toggle('active');
            console.log('Sidebar classes after toggle:', sidebar.classList);
        }
        if (mobileOverlay) {
            mobileOverlay.classList.toggle('active');
            console.log('Overlay classes after toggle:', mobileOverlay.classList);
        }
        document.body.classList.toggle('no-scroll');
    });
} else {
    console.error('menuToggle element not found!');
}
const modeToggle = document.getElementById('modeToggle');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const notificationBtn = document.getElementById('notificationBtn');
const notificationDropdown = document.getElementById('notificationDropdown');
const editProfileBtn = document.getElementById('editProfileBtn');
const editImageBtn = document.getElementById('editImageBtn');
const changePasswordBtn = document.getElementById('changePasswordBtn');
const enable2FABtn = document.getElementById('enable2FABtn');
const editProfileModal = document.getElementById('editProfileModal');
const changePasswordModal = document.getElementById('changePasswordModal');
const closeProfileModal = document.getElementById('closeProfileModal');
const cancelProfileBtn = document.getElementById('cancelProfileBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired');
    initializeDashboard();
    initializeCharts();
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute
});

// Alternative initialization in case DOMContentLoaded doesn't fire
if (document.readyState === 'loading') {
    console.log('Document still loading, waiting...');
} else {
    console.log('Document already loaded');
    initializeDashboard();
    initializeCharts();
    updateDateTime();
}

/* ============================================
   DARK MODE TOGGLE
   ============================================ */

function initializeDarkMode() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        modeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
}

modeToggle.addEventListener('click', () => {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    
    if (isDarkMode) {
        modeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('darkMode', 'true');
    } else {
        modeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('darkMode', 'false');
    }
});

// Initialize dark mode on load
initializeDarkMode();

/* ============================================
   SIDEBAR NAVIGATION
   ============================================ */

menuToggle.addEventListener('click', () => {
    console.log('Menu toggle clicked');
    sidebar.classList.toggle('active');
    mobileOverlay.classList.toggle('active');
    document.body.classList.toggle('no-scroll');
    console.log('Sidebar classes:', sidebar.classList);
});

// Close sidebar when overlay is clicked
if (mobileOverlay) {
    mobileOverlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        mobileOverlay.classList.remove('active');
        document.body.classList.remove('no-scroll');
    });
}

// Close sidebar when link is clicked
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Remove active class from all links
        navLinks.forEach(l => l.parentElement.classList.remove('active'));
        
        // Add active class to clicked link
        link.parentElement.classList.add('active');
        
        // Get the section to show
        const sectionId = link.getAttribute('data-section');
        showSection(sectionId);
        
        // Close sidebar on mobile
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
            mobileOverlay.classList.remove('active');
            document.body.classList.remove('no-scroll');
        }
    });
});

function showSection(sectionId) {
    // Hide all sections
    sections.forEach(section => {
        section.style.display = 'none';
    });
    
    // Show the selected section
    const selectedSection = document.getElementById(sectionId + '-section');
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

/* ============================================
   NOTIFICATIONS
   ============================================ */

notificationBtn.addEventListener('click', () => {
    notificationDropdown.style.display = notificationDropdown.style.display === 'none' ? 'block' : 'none';
});

// Close notification dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!notificationBtn.contains(e.target) && !notificationDropdown.contains(e.target)) {
        notificationDropdown.style.display = 'none';
    }
});

// Mark notification as read
document.querySelectorAll('.notification-item').forEach(item => {
    item.addEventListener('click', () => {
        item.classList.remove('unread');
    });
});

/* ============================================
   DATE & TIME
   ============================================ */

function updateDateTime() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateStr = now.toLocaleDateString('en-US', options);
    document.getElementById('headerDate').textContent = dateStr;
}

/* ============================================
   MODALS
   ============================================ */

// Edit Profile Modal
editProfileBtn.addEventListener('click', () => {
    editProfileModal.style.display = 'block';
    populateProfileForm();
});

closeProfileModal.addEventListener('click', () => {
    editProfileModal.style.display = 'none';
});

cancelProfileBtn.addEventListener('click', () => {
    editProfileModal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === editProfileModal) {
        editProfileModal.style.display = 'none';
    }
    if (e.target === changePasswordModal) {
        changePasswordModal.style.display = 'none';
    }
});

function populateProfileForm() {
    document.getElementById('modalFirstName').value = document.getElementById('fullName').textContent.split(' ')[0] || '';
    document.getElementById('modalLastName').value = document.getElementById('fullName').textContent.split(' ')[1] || '';
    document.getElementById('modalPhone').value = document.getElementById('phoneDisplay').textContent.replace('Not set', '') || '';
    document.getElementById('modalBio').value = '';
}

// Change Password Modal
changePasswordBtn.addEventListener('click', () => {
    changePasswordModal.style.display = 'block';
});

document.querySelectorAll('.close-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.target.closest('.modal').style.display = 'none';
    });
});

/* ============================================
   PROFILE IMAGE UPLOAD
   ============================================ */

editImageBtn.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = event.target.result;
                document.getElementById('profileImg').src = img;
                document.getElementById('headerProfileImg').src = img;
                localStorage.setItem('profileImage', img);
            };
            reader.readAsDataURL(file);
        }
    });
    input.click();
});

// Load saved profile image
window.addEventListener('load', () => {
    const savedImage = localStorage.getItem('profileImage');
    if (savedImage) {
        document.getElementById('profileImg').src = savedImage;
        document.getElementById('headerProfileImg').src = savedImage;
    }
});

/* ============================================
   FORM SUBMISSIONS
   ============================================ */

// Edit Profile Form
document.getElementById('editProfileForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const firstName = document.getElementById('modalFirstName').value;
    const lastName = document.getElementById('modalLastName').value;
    const phone = document.getElementById('modalPhone').value;
    const bio = document.getElementById('modalBio').value;
    
    // Update display
    document.getElementById('fullName').textContent = `${firstName} ${lastName}`;
    document.getElementById('phoneDisplay').textContent = phone || 'Not set';
    
    // Here you would send data to backend
    console.log('Profile updated:', { firstName, lastName, phone, bio });
    
    // Close modal
    editProfileModal.style.display = 'none';
    showNotification('Profile updated successfully!', 'success');
});

// Settings Form
document.querySelectorAll('.settings-form').forEach((form, index) => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        showNotification('Settings saved successfully!', 'success');
    });
});

/* ============================================
   ANALYTICS CHARTS
   ============================================ */

function initializeCharts() {
    // Views Chart
    const viewsCtx = document.getElementById('viewsChart');
    if (viewsCtx) {
        new Chart(viewsCtx, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
                datasets: [{
                    label: 'Views',
                    data: [1200, 1900, 1500, 2200, 1800, 2500, 3200],
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#00d4ff',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Clicks Chart
    const clicksCtx = document.getElementById('clicksChart');
    if (clicksCtx) {
        new Chart(clicksCtx, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
                datasets: [{
                    label: 'Clicks',
                    data: [250, 450, 350, 520, 480, 600, 750],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Device Distribution Chart
    const deviceCtx = document.getElementById('deviceChart');
    if (deviceCtx) {
        new Chart(deviceCtx, {
            type: 'doughnut',
            data: {
                labels: ['Mobile', 'Desktop', 'Tablet'],
                datasets: [{
                    data: [55, 35, 10],
                    backgroundColor: [
                        '#00d4ff',
                        '#667eea',
                        '#f39c12'
                    ],
                    borderColor: getComputedStyle(document.documentElement).getPropertyValue('--card'),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Traffic Sources Chart
    const sourceCtx = document.getElementById('sourceChart');
    if (sourceCtx) {
        new Chart(sourceCtx, {
            type: 'bar',
            data: {
                labels: ['Direct', 'Email', 'Social', 'Search', 'Referral'],
                datasets: [{
                    label: 'Traffic',
                    data: [450, 320, 280, 150, 120],
                    backgroundColor: [
                        '#00d4ff',
                        '#667eea',
                        '#43e97b',
                        '#fa709a',
                        '#fee140'
                    ],
                    borderRadius: 5
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}

/* ============================================
   NOTIFICATIONS
   ============================================ */

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    const style = document.createElement('style');
    if (!document.querySelector('style[data-notification]')) {
        style.setAttribute('data-notification', 'true');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                background: white;
                border-radius: 0.5rem;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
                z-index: 1000;
                animation: slideInRight 0.3s ease-out;
            }

            .notification-success {
                border-left: 4px solid #27ae60;
                color: #27ae60;
            }

            .notification-error {
                border-left: 4px solid #e74c3c;
                color: #e74c3c;
            }

            .notification-info {
                border-left: 4px solid #3498db;
                color: #3498db;
            }

            .notification-warning {
                border-left: 4px solid #f39c12;
                color: #f39c12;
            }

            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/* ============================================
   UTILITY FUNCTIONS
   ============================================ */

function initializeDashboard() {
    // Set first nav item as active
    if (navLinks.length > 0) {
        navLinks[0].parentElement.classList.add('active');
    }
    
    // Initialize dark mode
    initializeDarkMode();
}

// Handle window resize for sidebar
window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && sidebar.classList.contains('active')) {
        sidebar.classList.remove('active');
    }
});

/* ============================================
   2FA TOGGLE
   ============================================ */

enable2FABtn.addEventListener('click', () => {
    const badge = document.querySelector('#2faStatus .badge');
    if (badge.textContent === 'Disabled') {
        badge.textContent = 'Enabled';
        badge.classList.remove('badge-danger');
        badge.classList.add('badge-success');
        enable2FABtn.textContent = '✓ 2FA Enabled';
        enable2FABtn.disabled = true;
        showNotification('Two-Factor Authentication enabled successfully!', 'success');
    }
});

/* ============================================
   QUICK ACTION BUTTONS
   ============================================ */

// Create New Card
document.getElementById('createCardBtn')?.addEventListener('click', () => {
    showNotification('Redirecting to card creation...', 'info');
    // window.location.href = '/create-card/';
});

// View Visit Card
document.querySelectorAll('[class*="btn-secondary"]').forEach(btn => {
    if (btn.textContent.includes('View Card')) {
        btn.addEventListener('click', () => {
            showNotification('Opening your visit card...', 'info');
        });
    }
});

/* ============================================
   EXPORT DATA
   ============================================ */

document.querySelectorAll('.btn-danger').forEach(btn => {
    if (btn.textContent.includes('Export')) {
        btn.addEventListener('click', () => {
            showNotification('Preparing your data export...', 'info');
            // Simulate download
            setTimeout(() => {
                const data = {
                    profile: {
                        name: document.getElementById('fullName').textContent,
                        email: document.getElementById('emailDisplay').textContent,
                        phone: document.getElementById('phoneDisplay').textContent
                    },
                    timestamp: new Date().toISOString()
                };
                const link = document.createElement('a');
                link.href = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2));
                link.download = 'xlink-data.json';
                link.click();
                showNotification('Your data has been exported!', 'success');
            }, 1000);
        });
    }
});

/* ============================================
   DELETE ACCOUNT
   ============================================ */

document.querySelectorAll('.btn-danger').forEach(btn => {
    if (btn.textContent.includes('Delete')) {
        btn.addEventListener('click', () => {
            const confirmed = confirm('Are you sure you want to delete your account? This action cannot be undone.');
            if (confirmed) {
                const confirmed2 = confirm('This is permanent. All your data will be deleted. Continue?');
                if (confirmed2) {
                    showNotification('Account deletion initiated...', 'warning');
                }
            }
        });
    }
});

/* ============================================
   LOGOUT FROM OTHER SESSIONS
   ============================================ */

document.querySelectorAll('.btn-danger').forEach(btn => {
    if (btn.textContent.includes('Logout All')) {
        btn.addEventListener('click', () => {
            showNotification('Logging out from all other sessions...', 'info');
            setTimeout(() => {
                showNotification('All other sessions have been terminated!', 'success');
            }, 1500);
        });
    }
});

/* ============================================
   ANALYTICS FILTER
   ============================================ */

document.getElementById('dateRangeSelect')?.addEventListener('change', (e) => {
    const range = e.target.value;
    console.log('Date range changed to:', range);
    showNotification('Analytics updated for ' + range, 'info');
});

/* ============================================
   QR CODE GENERATION (Mock)
   ============================================ */

function generateQRCode() {
    // This would integrate with a QR code library
    // For now, it's just a placeholder
    console.log('QR Code would be generated here');
}

document.querySelectorAll('.btn').forEach(btn => {
    if (btn.textContent.includes('QR Code')) {
        btn.addEventListener('click', () => {
            showNotification('Downloading QR Code...', 'info');
        });
    }
});

/* ============================================
   PROFILE COMPLETION SIMULATION
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Simulate profile completion updates
    const completionCheckboxes = document.querySelectorAll('.check-item');
    completionCheckboxes.forEach((item, index) => {
        const icon = item.querySelector('i');
        // Randomly mark some as incomplete
        if (Math.random() > 0.7) {
            icon.className = 'fas fa-circle';
        }
    });
});

/* ============================================
   RESPONSIVE TABLE SCROLLING
   ============================================ */

const tables = document.querySelectorAll('table');
tables.forEach(table => {
    const wrapper = document.createElement('div');
    wrapper.style.overflowX = 'auto';
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
});
