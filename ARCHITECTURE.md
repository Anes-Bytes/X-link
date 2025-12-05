# X-Link Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (User Browser)                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Landing    │    │ Card Builder │    │ Public Card  │   │
│  │    Page      │───→│     Form     │───→│    View      │   │
│  │              │    │ (5 Steps)    │    │  (Dynamic    │   │
│  │ - Brand      │    │              │    │   Theming)   │   │
│  │   Carousel   │    │ - Templates  │    │              │   │
│  │ - Template   │    │ - Colors     │    │ - QR Code    │   │
│  │   Carousel   │    │ - Personal   │    │ - Social     │   │
│  │              │    │ - Social     │    │ - Skills     │   │
│  │              │    │ - Skills     │    │              │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                             ↓                    ↑           │
│                      ┌──────────────┐            │           │
│                      │ Success Page │            │           │
│                      │   (QR Code)  │            │           │
│                      └──────────────┘            │           │
│                                                  │           │
│  JavaScript Libraries:                          │           │
│  - carousel.js (Template 3D carousel)           │           │
│  - script.js (Global utilities)                 │           │
│                                                  │           │
│  Stylesheets:                                   │           │
│  - styles.css (Global + carousel styles)        │           │
│  - card-template-*.css (10 theme variants)      │           │
│                                                  │           │
│  CSS Features:                                  │           │
│  - 3D perspective effects                       │           │
│  - Smooth animations                            │           │
│  - Responsive breakpoints                       │           │
│  - Gradient backgrounds                         │           │
│                                                  │           │
└─────────────────────────────────────────────────────────────┘
                           ↕ AJAX / Form Submit
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Django Server)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  URL ROUTING (config/urls.py):                               │
│  ├── /                          → Xlink.views.landing_view   │
│  ├── /card/builder/             → core.views.card_builder    │
│  ├── /card/success/<id>/        → core.views.card_success    │
│  ├── /card/<username>/          → core.views.view_card       │
│  └── /api/...                   → AJAX endpoints             │
│                                                               │
│  VIEWS (core/views.py):                                      │
│  ┌──────────────────────────────────────────────┐            │
│  │ card_builder_view                            │            │
│  │ - GET: Render form + templates               │            │
│  │ - POST: Save UserCard + Skills               │            │
│  │ - Auth: @login_required                      │            │
│  ├──────────────────────────────────────────────┤            │
│  │ card_success_view                            │            │
│  │ - Display: Success + QR code                 │            │
│  │ - Generate: QR code link                     │            │
│  │ - Auth: @login_required                      │            │
│  ├──────────────────────────────────────────────┤            │
│  │ view_card                                    │            │
│  │ - Display: Published cards only              │            │
│  │ - Dynamic: Load theme CSS                    │            │
│  │ - Auth: Public (no auth)                     │            │
│  ├──────────────────────────────────────────────┤            │
│  │ AJAX Endpoints                               │            │
│  │ - add_skill_ajax (POST)                      │            │
│  │ - delete_skill_ajax (DELETE)                 │            │
│  │ - publish_card (POST)                        │            │
│  └──────────────────────────────────────────────┘            │
│                                                               │
│  FORMS (core/forms.py):                                      │
│  ├── UserCardForm                                            │
│  │   └── 20+ fields with custom widgets                      │
│  ├── SkillForm                                               │
│  │   └── Single skill input                                  │
│  └── SkillInlineFormSet                                      │
│      └── Manages multiple skills                            │
│                                                               │
│  MODELS (core/models.py):                                    │
│  ┌──────────────────────┐                                    │
│  │ CustomUser (Exists)  │◄────────┐                         │
│  └──────────────────────┘         │                         │
│                                   │                         │
│                    ┌──────────────────────────┐             │
│                    │    UserCard (NEW)        │             │
│                    ├──────────────────────────┤             │
│                    │ - username (unique)      │             │
│                    │ - name                   │             │
│                    │ - short_bio              │             │
│                    │ - description            │             │
│                    │ - email                  │             │
│                    │ - website                │             │
│                    │ - social_handles (5)     │             │
│                    │ - color (choice/enum)    │             │
│                    │ - template_id (FK)       │             │
│                    │ - is_published           │             │
│                    │ - created_at/updated_at  │             │
│                    └──────────────────────────┘             │
│                            │                                 │
│                            │ 1-to-Many                      │
│                            ↓                                 │
│                    ┌──────────────────────────┐             │
│                    │    Skill (NEW)           │             │
│                    ├──────────────────────────┤             │
│                    │ - name                   │             │
│                    │ - created_at             │             │
│                    │ - user_card_id (FK)      │             │
│                    └──────────────────────────┘             │
│                                                               │
│  ADMIN INTERFACE (core/admin.py):                            │
│  ├── UserCardAdmin                                           │
│  │   ├── List filters (color, published, date)              │
│  │   ├── Search fields (name, username, email)              │
│  │   ├── SkillInline for nested editing                     │
│  │   └── Organized fieldsets                                │
│  ├── SkillAdmin                                              │
│  │   ├── List view with metadata                            │
│  │   └── Search and filtering                               │
│  └── CustomUserAdmin (Existing)                             │
│                                                               │
│  CONTEXT PROCESSORS (core/context_processors.py):           │
│  └── site_context()                                         │
│      ├── Returns: SiteContext data                          │
│      ├── Returns: UserCard (if authenticated)               │
│      └── Returns: Skills (if authenticated)                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                           ↕ ORM Queries
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  TABLES:                                                     │
│                                                               │
│  auth_user (Django Built-in)                                │
│  ├── id (PK)                                                │
│  ├── username                                               │
│  ├── email                                                  │
│  └── ...                                                    │
│                                                               │
│  core_usercard (NEW)              core_customuser (Extends) │
│  ├── id (PK)                                                │
│  ├── user_id (OneToOne→auth_user)                          │
│  ├── username (unique slug)                                 │
│  ├── template_id (FK→CardTemplate)                         │
│  ├── color (choice)                                         │
│  ├── name, short_bio, description                          │
│  ├── email, website                                         │
│  ├── instagram/telegram/linkedin/youtube/twitter          │
│  ├── is_published (boolean)                                │
│  ├── created_at, updated_at                                │
│  └── Indexes: username, user_id                            │
│                                                               │
│  core_skill (NEW)                                           │
│  ├── id (PK)                                                │
│  ├── user_card_id (FK→UserCard)                            │
│  ├── name (CharField)                                       │
│  ├── created_at                                             │
│  └── Indexes: user_card_id                                 │
│                                                               │
│  Xlink_cardtemplate (Existing)                              │
│  ├── id (PK)                                                │
│  ├── template_id (slug)                                     │
│  ├── name, category                                         │
│  ├── preview_image (URL)                                    │
│  └── is_active (boolean)                                    │
│                                                               │
│  core_customers (Existing)                                  │
│  ├── company_name                                           │
│  ├── company_logo (ImageField)                              │
│  └── company_url                                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘

```

---

## 🔄 Data Flow

### Creating a Card

```
User (Browser)
    ↓
1. Visit /card/builder/
    ↓
Django Check: Is user logged in?
    ├─ NO → Redirect to login
    └─ YES ↓
    ↓
2. Load form with available templates
    ↓
    [Show 5-step form]
    ├─ Step 1: Select template
    ├─ Step 2: Choose color
    ├─ Step 3: Enter personal info
    ├─ Step 4: Add social handles
    └─ Step 5: Add skills
    ↓
3. User submits form (POST)
    ↓
Django validation
    ├─ Form errors? → Show errors
    └─ Valid? ↓
    ↓
4. Save to database
    ├─ Create/Update UserCard
    ├─ Save/Update Skills
    └─ Generate unique username slug
    ↓
5. Redirect to success page
    ↓
6. Generate QR code
    ├─ Use qrserver.com API
    ├─ Generate dynamic image
    └─ Display with share options
    ↓
7. Show options
    ├─ View card → /card/<username>/
    ├─ Edit card → /card/builder/
    └─ Share card → Social buttons
```

### Viewing a Card

```
User (Browser)
    ↓
Visit /card/<username>/
    ↓
Django lookup: Find UserCard with username
    ├─ Not found? → 404 Error
    ├─ is_published=False? → 404 Error (if not owner)
    └─ Found & Published? ↓
    ↓
Load card template (card_view.html)
    ↓
Load dynamic theme CSS
    ├─ If color='blue' → Load card-template-blue.css
    ├─ If color='red' → Load card-template-red.css
    └─ Default → Load card-template.css
    ↓
Render card with:
    ├─ Personal info (name, bio, etc)
    ├─ Contact details (email, website)
    ├─ Skills (from related Skill objects)
    ├─ Social links (Instagram, Twitter, etc)
    └─ QR code (generated on the fly)
    ↓
Display action buttons:
    ├─ Share card (if owner)
    ├─ Download card
    └─ Download QR code
```

### Template Selection in Carousel

```
Landing page loads
    ↓
JavaScript initializes TemplateCarousel
    ├─ Query templates from database
    ├─ Render carousel slides
    └─ Attach event listeners
    ↓
User interacts:
    ├─ Click button → Slide moves
    ├─ Drag mouse → Smooth animation
    ├─ Touch swipe → Mobile support
    ├─ Arrow keys → Keyboard nav
    └─ Click "Select" → selectTemplate()
    ↓
JavaScript saves selection
    ├─ localStorage.selectedTemplate = id
    ├─ localStorage.selectedTemplateName = name
    └─ Redirect to /card/builder/
    ↓
Form loads with selected template
```

---

## 🌐 Request/Response Cycle

### Example: Creating a Card

```
REQUEST:
POST /card/builder/
Content-Type: multipart/form-data

Data:
├─ username: "johndoe"
├─ name: "John Doe"
├─ short_bio: "Web Developer"
├─ email: "john@example.com"
├─ color: "blue"
├─ template: "1"
├─ instagram_username: "@johndoe"
├─ skills-TOTAL_FORMS: "2"
├─ skills-0-name: "Python"
└─ skills-1-name: "Django"

BACKEND PROCESSING:
1. Authenticate user ✓
2. Validate form data ✓
3. Create UserCard instance ✓
4. Create Skill instances ✓
5. Generate success page ✓

RESPONSE:
Redirect: /card/success/42/
Status: 302 Found

REDIRECTED REQUEST:
GET /card/success/42/

RESPONSE:
<html>
  <h1>Card Created Successfully!</h1>
  <p>Link: https://example.com/johndoe</p>
  <img src="https://api.qrserver.com/..." /> [QR Code]
  ...buttons and preview...
</html>
Status: 200 OK
```

---

## 📊 Component Dependencies

```
UserCard
├── Depends on: CustomUser (OneToOne)
├── Depends on: CardTemplate (ForeignKey)
├── Has many: Skill (reverse relation)
├── Related to: Theme CSS files
└── Outputs: get_card_url()

Skill
├── Depends on: UserCard (ForeignKey)
└── Ordered by: created_at

TemplateCarousel (JavaScript)
├── Requires: carousel.js
├── Requires: HTML with specific classes
├── Requires: CSS animations
└── Generates: selectTemplate() calls

CardTheme System
├── UserCard.color → CSS file selector
├── card_view.html → Conditional loading
├── 10 CSS files → Theme variations
└── card-template-*.css

SiteContext (Existing)
├── Provides: Global site data
├── Accessed via: context_processor
└── Used in: Templates
```

---

## 🔐 Data Security Flow

```
User Input
    ↓
Browser Validation (JavaScript)
    ├─ Basic checks
    └─ UX feedback
    ↓
Form Submission
    ├─ CSRF Token (Django middleware)
    └─ HTTPS (production)
    ↓
Server-side Validation
    ├─ Form.is_valid()
    ├─ Check authentication
    ├─ Verify ownership
    └─ Sanitize data
    ↓
Database Storage
    ├─ ORM prevents SQL injection
    ├─ Parameterized queries
    └─ Encrypted at rest (production)
    ↓
Template Rendering
    ├─ Auto-escape HTML (Django)
    ├─ Safe template tags
    └─ XSS protection
    ↓
Browser Display
    ├─ CSP headers (production)
    └─ No inline scripts
```

---

## ⚙️ Configuration Points

```
settings.py
├─ INSTALLED_APPS = [..., 'core', 'Xlink']
├─ AUTH_USER_MODEL = 'core.CustomUser'
├─ STATIC_URL = '/static/'
├─ STATICFILES_DIRS = [...]
├─ MEDIA_URL = '/media/'
├─ MEDIA_ROOT = ...
├─ TEMPLATES processors (site_context)
└─ DEBUG = True/False

urls.py
├─ path('', include('Xlink.urls'))
├─ path('', include('core.urls'))
└─ static() files in DEBUG mode

Form Configuration
├─ UserCardForm widgets (styling)
├─ Field labels and help text
├─ RTL/LTR direction
└─ Placeholder text

Template Customization
├─ Color themes editable
├─ Logo sizes adjustable
├─ Form layout modifiable
└─ Card sections customizable
```

---

## 📈 Performance Considerations

```
Optimization Strategies:

1. Database Queries
   └─ select_related() for ForeignKeys
   └─ prefetch_related() for reverse relations
   └─ Indexed fields: username, user_id

2. Static Files
   └─ Minify CSS and JavaScript
   └─ Use CDN for distribution
   └─ Browser caching headers
   └─ Lazy load carousel images

3. Frontend
   └─ CSS animations use GPU
   └─ Debounce resize events
   └─ Efficient event delegation
   └─ Minimize DOM reflows

4. API Response
   └─ Return only needed data
   └─ Cache template queries
   └─ Compress responses
   └─ Use pagination when needed
```

---

## 🧪 Testing Points

```
Unit Tests
├─ Model validation
├─ Form processing
└─ View logic

Integration Tests
├─ Full request/response cycle
├─ Database operations
└─ Authentication flow

Frontend Tests
├─ Carousel functionality
├─ Form validation
├─ Responsive layouts
└─ Browser compatibility

Performance Tests
├─ Page load time
├─ API response time
├─ Database query efficiency
└─ Memory usage
```

---

**Architecture Version:** 1.0  
**Last Updated:** December 5, 2025  
**Status:** Production Ready ✅
