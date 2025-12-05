# 🚀 X-Link Quick Reference Card

## 📍 Key URLs

| URL | Purpose | Auth |
|-----|---------|------|
| `/` | Landing page | Public |
| `/admin/` | Admin panel | Admin |
| `/card/builder/` | Create/edit card | Required |
| `/card/success/<id>/` | Success page | Required |
| `/card/<username>/` | View public card | Public |

---

## 🎨 Color Themes

```python
COLOR_CHOICES = [
    'default',   # card-template.css
    'blue',      # card-template-blue.css
    'gold',      # card-template-gold.css
    'orange',    # card-template-orange.css
    'gray',      # card-template-gray.css
    'mint',      # card-template-mint.css
    'pink',      # card-template-pink.css
    'purple',    # card-template-purple.css
    'red',       # card-template-red.css
    'green',     # card-template-green.css
]
```

---

## 📝 Model Fields

### UserCard
```python
user                      # OneToOne CustomUser
username                  # unique slug
template                  # FK CardTemplate
color                     # choice (10 options)
name, short_bio          # text fields
description              # text field
email, website           # URL fields
instagram_username       # social handle
telegram_username        # social handle
linkedin_username        # social handle
youtube_username         # social handle
twitter_username         # social handle
is_published             # boolean
created_at, updated_at   # timestamps
```

### Skill
```python
user_card   # FK UserCard
name        # CharField
created_at  # timestamp
```

---

## 🔌 API Endpoints

### Card Operations
- `POST /card/builder/` - Create/update card
- `GET /card/success/<id>/` - Success page
- `GET /card/<username>/` - View public card

### Skills (AJAX)
- `POST /api/skill/add/` - Add skill
- `DELETE /api/skill/<id>/delete/` - Remove skill
- `POST /api/card/<id>/publish/` - Publish card

---

## 💻 Admin URLs

```
/admin/core/usercard/       - Manage user cards
/admin/core/skill/          - Manage skills
/admin/xlink/cardtemplate/  - Manage templates
/admin/core/customers/      - Manage brand logos
```

---

## 🎯 Quick Start

### 1. Create Superuser
```bash
python manage.py createsuperuser
```

### 2. Add Template Data
Visit `/admin/` → Xlink → Card templates → Add template

### 3. Start Server
```bash
python manage.py runserver
```

### 4. Visit Landing
`http://localhost:8000/`

---

## 🔧 Key Files

**Backend:**
- `core/models.py` - UserCard, Skill models
- `core/forms.py` - Forms and formsets
- `core/views.py` - View functions
- `core/urls.py` - URL routing
- `core/admin.py` - Admin configuration

**Frontend:**
- `static/carousel.js` - Carousel component
- `static/styles.css` - Global styles (brand + carousel)
- `core/templates/core/` - Card templates

**Templates:**
- `card_builder.html` - Form
- `card_success.html` - Success page
- `card_view.html` - Public view

---

## 📱 Responsive Breakpoints

```css
/* Mobile < 480px */
/* Tablet 480px - 768px */
/* Desktop > 768px */
```

---

## 🎨 JavaScript Classes

### TemplateCarousel
```javascript
new TemplateCarousel('.templates-carousel', {
    autoPlay: false,
    autoPlayInterval: 5000
});

// Methods:
carousel.prev()           // Previous slide
carousel.next()           // Next slide
carousel.selectSlide(0)   // Go to slide 0
```

### Helper Functions
```javascript
selectTemplate(id, name)   // Select template & redirect
copyToClipboard(text)      // Copy text
downloadQRCode()           // Download QR code
```

---

## 🔐 Authentication

```python
@login_required
def card_builder_view(request):
    # User must be authenticated
    user_card = UserCard.objects.get(user=request.user)
```

---

## 📊 Database Tables

```
auth_user           ← CustomUser (extends)
    ↓
core_usercard       ← UserCard (OneToOne)
    ↓
core_skill          ← Skill (ForeignKey)

Xlink_cardtemplate  ← Referenced by UserCard
```

---

## 🎓 Form Steps

1. **Template Selection** - Choose from available templates
2. **Color Theme** - Select from 10 colors
3. **Personal Info** - Name, bio, email, website
4. **Social Media** - Instagram, Telegram, LinkedIn, YouTube, Twitter
5. **Skills** - Add/remove unlimited skills

---

## ⚙️ Settings

```python
# settings.py
INSTALLED_APPS = [..., 'core', 'Xlink']
AUTH_USER_MODEL = 'core.CustomUser'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
```

---

## 🧪 Testing Commands

```bash
# Check configuration
python manage.py check

# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

---

## 🎨 Carousel Features

- **3D Depth Effect** - Uses CSS perspective
- **Smooth Animations** - cubic-bezier timing
- **Mouse Drag** - 50px threshold
- **Touch/Swipe** - Mobile support
- **Keyboard Nav** - Arrow keys
- **Center Emphasis** - Scale effect
- **Hover Lift** - Visual feedback
- **Responsive** - Auto-sizing

---

## 📈 QR Code

**API:** `qrserver.com`

**Format:**
```
https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=<url>
```

**Sizes:**
- Display: 300×300
- Download: 500×500

---

## 🔒 Security Features

- CSRF protection (forms)
- XSS prevention (template escaping)
- SQL injection prevention (ORM)
- Authentication required (views)
- Authorization checks (ownership verification)
- Form validation (client + server)

---

## 📚 Documentation Files

```
X-link/
├── IMPLEMENTATION_GUIDE.md    - Complete technical guide
├── TESTING_GUIDE.md           - Testing instructions
├── FILES_SUMMARY.md           - File changes
├── ARCHITECTURE.md            - System architecture
└── VERIFICATION_CHECKLIST.md  - Complete checklist
```

---

## 🚀 Deployment

```bash
# Set DEBUG = False
# Collect static files
python manage.py collectstatic --clear

# Configure production settings
# Set ALLOWED_HOSTS
# Enable HTTPS
# Set secure cookies
```

---

## 🆘 Common Issues

**Carousel not moving?**
- Clear cache (Ctrl+Shift+Del)
- Check console for errors
- Verify carousel.js is loaded

**QR code not showing?**
- Check internet connection
- Verify URL format
- Test API directly

**Theme not changing?**
- Clear static files
- Verify CSS files exist
- Check UserCard.color value

**Form won't submit?**
- Check browser console
- Verify required fields filled
- Check CSRF token present

---

## 💡 Tips & Tricks

### Get Card URL
```python
card = UserCard.objects.get(username='john')
url = card.get_card_url()
```

### Check User's Card
```python
user = User.objects.get(username='john')
card = user.user_card
```

### Get All Skills
```python
card = UserCard.objects.get(id=1)
skills = card.skills.all()
```

### Create Card in Admin
```
/admin/core/usercard/add/
```

---

## 📊 Performance Tips

- Use `select_related()` for ForeignKeys
- Cache template queries
- Minify CSS/JS for production
- Use CDN for static files
- Lazy load carousel images
- Enable gzip compression

---

## 🎯 Feature Checklist

- [x] Responsive brand section
- [x] Template carousel
- [x] Card builder form
- [x] Dynamic skills
- [x] Success page with QR
- [x] Public card view
- [x] 10 color themes
- [x] Responsive design
- [x] Admin interface
- [x] Security measures

---

## 📞 Support Resources

- Django Docs: https://docs.djangoproject.com/
- X-Link Docs: See IMPLEMENTATION_GUIDE.md
- Troubleshooting: See TESTING_GUIDE.md
- Architecture: See ARCHITECTURE.md

---

**Last Updated:** December 5, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready  

Keep this card handy for quick reference!
