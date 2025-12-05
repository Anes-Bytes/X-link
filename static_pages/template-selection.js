/* ============================================
   داده‌های نمونه + بارگذاری از API
   ============================================ */
const fallbackTemplates = [
    {
        templateId: 'xr-neon-01',
        name: 'نئون پالس',
        category: 'neon',
        categoryLabel: 'نئون / آینده‌گرا',
        visualStyle: 'glow',
        description: 'نمایشگر تمام‌صفحه با خطوط نئون، مناسب برندهای تکنولوژی و استارتاپ‌های آینده‌نگر.',
        previewImage: 'https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=900&q=80',
        customizationOptions: {
            backgroundColors: ['#050714', '#0A0F1F', '#140032'],
            accentColors: ['#3A86FF', '#00F6FF', '#FF5F9E'],
            effects: {
                neonGlow: true,
                shootingStars: true,
                particles: true,
                gradientOverlay: true,
                textureLayer: false
            }
        }
    },
    {
        templateId: 'xr-minimal-02',
        name: 'مینیمال هارمونی',
        category: 'minimal',
        categoryLabel: 'مینیمال',
        visualStyle: 'minimal',
        description: 'طراحی تمیز با خطوط دقیق و تایپوگرافی ظریف برای حرفه‌ای‌های محتاط.',
        previewImage: 'https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?auto=format&fit=crop&w=900&q=80',
        customizationOptions: {
            backgroundColors: ['#0D111F', '#121826', '#1F2437'],
            accentColors: ['#3A86FF', '#7B61FF', '#A5F3FC'],
            effects: {
                neonGlow: false,
                shootingStars: false,
                particles: true,
                gradientOverlay: true,
                textureLayer: true
            }
        }
    },
    {
        templateId: 'xr-cyber-03',
        name: 'سایبر دارک',
        category: 'dark',
        categoryLabel: 'سایبر / تیره',
        visualStyle: 'cyber',
        description: 'بافت‌های دیجیتال با حس متاورسی، ترکیبی از شبکه‌های هندسی و گرادینت سرد.',
        previewImage: 'https://images.unsplash.com/photo-1488229297570-58520851e868?auto=format&fit=crop&w=900&q=80',
        customizationOptions: {
            backgroundColors: ['#010409', '#050D1E', '#0F172A'],
            accentColors: ['#00F6FF', '#64FFDA', '#38BDF8'],
            effects: {
                neonGlow: true,
                shootingStars: false,
                particles: true,
                gradientOverlay: true,
                textureLayer: true
            }
        }
    },
    {
        templateId: 'xr-corporate-04',
        name: 'کورپریت تراست',
        category: 'corporate',
        categoryLabel: 'حرفه‌ای / شرکتی',
        visualStyle: 'corporate',
        description: 'قالب رسمی با ساختار دو ستونه و فضای کافی برای اطلاعات تماس و شبکه اجتماعی.',
        previewImage: 'https://images.unsplash.com/photo-1483478550801-ceba5fe50e8e?auto=format&fit=crop&w=900&q=80',
        customizationOptions: {
            backgroundColors: ['#0B1222', '#0E162A', '#101B33'],
            accentColors: ['#3A86FF', '#1D4ED8', '#10B981'],
            effects: {
                neonGlow: false,
                shootingStars: false,
                particles: false,
                gradientOverlay: true,
                textureLayer: true
            }
        }
    },
    {
        templateId: 'xr-gradient-05',
        name: 'گرادینت ریف',
        category: 'gradient',
        categoryLabel: 'گرادینت',
        visualStyle: 'gradient',
        description: 'پس‌زمینه‌های سیال با گرادینت‌های چند‌رنگ و کارت شیشه‌ای شناور.',
        previewImage: 'https://images.unsplash.com/photo-1526318896980-cf78c088247c?auto=format&fit=crop&w=900&q=80',
        customizationOptions: {
            backgroundColors: ['#130F40', '#1F1147', '#2D0B52'],
            accentColors: ['#FF5F9E', '#FFB347', '#5DE0E6'],
            effects: {
                neonGlow: true,
                shootingStars: false,
                particles: true,
                gradientOverlay: true,
                textureLayer: false
            }
        }
    }
];

const effectLabels = {
    neonGlow: 'نور نئونی',
    shootingStars: 'ستاره‌های دنباله‌دار',
    particles: 'ذرات شناور',
    gradientOverlay: 'لایه گرادینت',
    textureLayer: 'بافت هندسی'
};

let templatesData = [];
let filteredTemplates = [];
let activeCategory = 'all';
let activeTemplate = null;
let customizationState = {
    backgroundColor: '#0A0F1F',
    accentColor: '#3A86FF',
    effects: {
        neonGlow: true,
        shootingStars: false,
        particles: false,
        gradientOverlay: true,
        textureLayer: false
    }
};

/* ============================================
   المان‌های DOM
   ============================================ */
const categoryToolbar = document.getElementById('categoryToolbar');
const sliderTrack = document.getElementById('templateSliderTrack');
const sliderPagination = document.getElementById('sliderPagination');
const sliderPrev = document.getElementById('sliderPrev');
const sliderNext = document.getElementById('sliderNext');
const backgroundColorInput = document.getElementById('backgroundColor');
const backgroundColorValue = document.getElementById('backgroundColorValue');
const accentColorInput = document.getElementById('accentColor');
const accentColorValue = document.getElementById('accentColorValue');
const effectList = document.getElementById('effectList');
const previewWrapper = document.getElementById('livePreview');
const previewCard = previewWrapper.querySelector('.preview-card');
const previewName = document.getElementById('previewName');
const previewRole = document.getElementById('previewRole');
const previewStyle = document.getElementById('previewStyle');
const previewDescription = document.getElementById('previewDescription');
const previewCategory = document.getElementById('previewCategory');
const previewId = document.getElementById('previewId');
const confirmButton = document.getElementById('confirmTemplate');
const resetButton = document.getElementById('resetCustomization');
const selectionStatus = document.getElementById('selectionStatus');

/* ============================================
   بارگذاری داده‌ها
   ============================================ */
async function loadTemplates() {
    try {
        const response = await fetch('/api/templates/');
        if (!response.ok) throw new Error('network');
        const payload = await response.json();
        templatesData = payload.templates?.length ? payload.templates : fallbackTemplates;
    } catch (error) {
        console.warn('template api fallback', error);
        templatesData = fallbackTemplates;
    }

    filteredTemplates = [...templatesData];
    renderCategories();
    renderTemplates();
    if (filteredTemplates.length) {
        setActiveTemplate(filteredTemplates[0].templateId);
    }
}

/* ============================================
   تولید دسته‌بندی‌ها
   ============================================ */
function renderCategories() {
    const categories = Array.from(new Set(templatesData.map(t => t.category)));
    const labels = {
        all: 'همه قالب‌ها',
        minimal: 'مینیمال',
        dark: 'سایبر / تیره',
        neon: 'نئون / آینده‌گرا',
        corporate: 'حرفه‌ای / شرکتی',
        gradient: 'گرادینت',
        creative: 'خلاق / مدرن'
    };

    const fragment = document.createDocumentFragment();

    const allBtn = createCategoryButton('all', labels.all);
    fragment.appendChild(allBtn);

    categories.forEach(category => {
        const persianLabel = labels[category] || category;
        fragment.appendChild(createCategoryButton(category, persianLabel));
    });

    categoryToolbar.innerHTML = '';
    categoryToolbar.appendChild(fragment);
    updateActiveCategoryButton();
}

function createCategoryButton(value, label) {
    const button = document.createElement('button');
    button.className = 'category-pill';
    button.dataset.category = value;
    button.textContent = label;
    button.addEventListener('click', () => {
        activeCategory = value;
        filteredTemplates = value === 'all'
            ? [...templatesData]
            : templatesData.filter(t => t.category === value);
        renderTemplates();
        updateActiveCategoryButton();
        if (filteredTemplates.length) {
            setActiveTemplate(filteredTemplates[0].templateId);
        }
    });
    return button;
}

function updateActiveCategoryButton() {
    const buttons = categoryToolbar.querySelectorAll('.category-pill');
    buttons.forEach(button => {
        button.classList.toggle('active', button.dataset.category === activeCategory);
    });
}

/* ============================================
   رندر اسلایدر قالب‌ها
   ============================================ */
function renderTemplates() {
    sliderTrack.innerHTML = '';
    filteredTemplates.forEach(template => {
        const card = document.createElement('article');
        card.className = 'template-card-large';
        card.dataset.id = template.templateId;
        card.innerHTML = `
            <div class="template-preview-image">
                <img src="${template.previewImage}" alt="${template.name}">
            </div>
            <div class="template-info">
                <div class="template-meta">
                    <span class="category-badge">${template.categoryLabel || template.category}</span>
                    <span class="style-tag">${template.visualStyle}</span>
                </div>
                <h3>${template.name}</h3>
                <p>${template.description}</p>
                <div class="template-actions">
                    <span class="template-id">${template.templateId.toUpperCase()}</span>
                    <button type="button">انتخاب قالب</button>
                </div>
            </div>
        `;
        card.querySelector('button').addEventListener('click', () => setActiveTemplate(template.templateId));
        sliderTrack.appendChild(card);
    });

    updateActiveCard();
    updatePagination();
}

function updateActiveCard() {
    const cards = sliderTrack.querySelectorAll('.template-card-large');
    cards.forEach(card => {
        card.classList.toggle('active', card.dataset.id === activeTemplate?.templateId);
    });
}

function updatePagination() {
    sliderPagination.innerHTML = '';
    filteredTemplates.forEach(template => {
        const dot = document.createElement('span');
        dot.className = 'pagination-dot';
        dot.classList.toggle('active', template.templateId === activeTemplate?.templateId);
        dot.addEventListener('click', () => setActiveTemplate(template.templateId));
        sliderPagination.appendChild(dot);
    });
}

/* ============================================
   مدیریت قالب فعال
   ============================================ */
function setActiveTemplate(templateId) {
    const template = filteredTemplates.find(t => t.templateId === templateId) ||
        templatesData.find(t => t.templateId === templateId);
    if (!template) return;

    activeTemplate = template;
    previewName.textContent = template.name;
    previewRole.textContent = template.visualStyle;
    previewStyle.textContent = template.categoryLabel || template.category;
    previewDescription.textContent = template.description;
    previewCategory.textContent = template.categoryLabel || template.category;
    previewId.textContent = template.templateId.toUpperCase();

    customizationState.backgroundColor = template.customizationOptions.backgroundColors[0];
    customizationState.accentColor = template.customizationOptions.accentColors[0];
    customizationState.effects = {
        ...customizationState.effects,
        ...template.customizationOptions.effects
    };

    backgroundColorInput.value = customizationState.backgroundColor;
    backgroundColorValue.textContent = customizationState.backgroundColor.toUpperCase();
    accentColorInput.value = customizationState.accentColor;
    accentColorValue.textContent = customizationState.accentColor.toUpperCase();

    renderEffects(template.customizationOptions.effects);
    updatePreview();
    updateActiveCard();
    updatePagination();
}

function renderEffects(effects) {
    effectList.innerHTML = '';
    Object.keys(effectLabels).forEach(effectKey => {
        const isSupported = effects[effectKey];
        const listItem = document.createElement('li');
        listItem.className = 'effect-item';
        listItem.innerHTML = `
            <label>${effectLabels[effectKey]}</label>
            <label class="toggle-switch">
                <input type="checkbox" ${isSupported ? 'checked' : 'disabled'}>
                <span class="toggle-slider"></span>
            </label>
        `;
        const checkbox = listItem.querySelector('input');
        if (isSupported) {
            checkbox.checked = customizationState.effects[effectKey];
            checkbox.addEventListener('change', () => {
                customizationState.effects[effectKey] = checkbox.checked;
                updatePreview();
            });
        }
        effectList.appendChild(listItem);
    });
}

/* ============================================
   پیش‌نمایش زنده
   ============================================ */
function updatePreview() {
    previewCard.style.background = `linear-gradient(135deg, ${hexToRgba(customizationState.backgroundColor, 0.9)}, ${hexToRgba(customizationState.accentColor, 0.35)})`;
    previewCard.style.borderColor = customizationState.accentColor;
    previewCard.classList.toggle('glow', customizationState.effects.neonGlow);

    previewWrapper.classList.toggle('shooting-stars', customizationState.effects.shootingStars);
    previewWrapper.classList.toggle('particle-overlay', customizationState.effects.particles);
    previewWrapper.classList.toggle('gradient-overlay', customizationState.effects.gradientOverlay);
    previewWrapper.classList.toggle('texture-layer', customizationState.effects.textureLayer);
}

function hexToRgba(hex, alpha = 1) {
    const trimmed = hex.replace('#', '');
    const bigint = parseInt(trimmed, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

/* ============================================
   کنترل‌های رنگ
   ============================================ */
backgroundColorInput.addEventListener('input', () => {
    customizationState.backgroundColor = backgroundColorInput.value;
    backgroundColorValue.textContent = backgroundColorInput.value.toUpperCase();
    updatePreview();
});

accentColorInput.addEventListener('input', () => {
    customizationState.accentColor = accentColorInput.value;
    accentColorValue.textContent = accentColorInput.value.toUpperCase();
    updatePreview();
});

resetButton.addEventListener('click', () => {
    if (!activeTemplate) return;
    setActiveTemplate(activeTemplate.templateId);
    selectionStatus.textContent = '';
});

/* ============================================
   ناوبری اسلایدر
   ============================================ */
sliderPrev.addEventListener('click', () => {
    sliderTrack.scrollBy({ left: -400, behavior: 'smooth' });
});

sliderNext.addEventListener('click', () => {
    sliderTrack.scrollBy({ left: 400, behavior: 'smooth' });
});

/* ============================================
   ذخیره انتخاب قالب
   ============================================ */
confirmButton.addEventListener('click', async () => {
    if (!activeTemplate) return;
    selectionStatus.textContent = 'در حال ذخیره‌سازی انتخاب...';
    selectionStatus.className = 'selection-status';

    const payload = {
        template_id: activeTemplate.templateId,
        customization: customizationState
    };

    try {
        const response = await fetch('/api/templates/select/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('network');
        selectionStatus.textContent = 'قالب انتخاب شد! انتقال به مرحله ساخت کارت...';
        selectionStatus.classList.add('success');

        setTimeout(() => {
            window.location.href = 'create.html';
        }, 1000);
    } catch (error) {
        console.warn('selection fallback', error);
        localStorage.setItem('xlinkSelectedTemplate', JSON.stringify(payload));
        selectionStatus.textContent = 'ذخیره در حالت آفلاین انجام شد. پس از ورود به مرحله بعد، داده‌ها بارگذاری می‌شوند.';
        selectionStatus.classList.add('success');
    }
});

/* ============================================
   راه‌اندازی اولیه
   ============================================ */
document.addEventListener('DOMContentLoaded', () => {
    loadTemplates();
});



