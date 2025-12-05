# X-Link Implementation - Quick Testing Guide

## ✅ What Has Been Implemented

### 1. **Backend Database Models** ✅
- **UserCard Model** - Stores user digital card data with all required fields
- **Skill Model** - Dynamic skills associated with each user card
- **Color Choices** - 10 color themes: default, blue, gold, orange, gray, mint, pink, purple, red, green

### 2. **Frontend Features** ✅

#### 🎨 Landing Page Enhancements:
- **Dynamic Brand Section** - Infinite scrolling carousel with responsive logos
- **Template Carousel** - Interactive 3D carousel with:
  - Mouse drag support
  - Touch/swipe support
  - Keyboard navigation (arrow keys)
  - Smooth depth effect animations
  - Centered template emphasis

#### 📝 Card Builder (5-Step Form):
1. **Template Selection** - Grid-based template selection with preview images
2. **Color Theme** - Dropdown to select from 10 color themes
3. **Personal Info** - Name, bio, description, email, website
4. **Social Media** - Instagram, Telegram, LinkedIn, YouTube, Twitter
5. **Dynamic Skills** - Add unlimited skills with add/remove buttons

#### ✨ Success Page:
- Shareable card link (copy to clipboard)
- **Dynamic QR Code** (auto-generated using qrserver.com)
- Card preview
- Social sharing buttons (Telegram, WhatsApp, Twitter, Email)
- Download QR code functionality

#### 🔗 Public Card View:
- Dynamic theme CSS loading based on user selection
- Responsive card design
- All social media links
- Skills display
- QR code for sharing
- Action buttons (Share, Download, QR)

### 3. **Backend Implementation** ✅

#### Forms (`core/forms.py`):
- UserCardForm with custom widgets
- SkillForm for inline editing
- SkillInlineFormSet for managing multiple skills

#### Views (`core/views.py`):
- `card_builder_view` - Create/edit card
- `card_success_view` - Success page with QR
- `view_card` - Public card display
- AJAX endpoints for dynamic skill management

#### URL Routing (`core/urls.py`):
```
/card/builder/                - Card creation
/card/success/<id>/           - Success page
/card/<username>/             - Public view
/api/skill/add/               - Add skill (AJAX)
/api/skill/<id>/delete/       - Remove skill (AJAX)
/api/card/<id>/publish/       - Publish card (AJAX)
```

#### Admin Interface (`core/admin.py`):
- UserCardAdmin with inline skills
- SkillAdmin
- List filters and search capabilities

### 4. **Responsive Design** ✅
- Mobile First approach
- Tablet optimizations (768px breakpoint)
- Desktop enhancements (1024px+)
- Flexible layouts using CSS Grid and Flexbox
- Touch-friendly interactive elements

### 5. **CSS Styling** ✅
- Brand section responsive carousel
- Template carousel with 3D effects
- Form styling with animations
- Success page with gradient effects
- Public card view with theme integration

---

## 🧪 Testing Instructions

### Step 1: Run Development Server
```bash
python manage.py runserver
```

### Step 2: Create Test User (if needed)
```bash
python manage.py createsuperuser
# Then login at /admin/
```

### Step 3: Create Template Data
Visit `/admin/` and add some `CardTemplate` entries:
- Go to **Xlink > Card templates**
- Create templates with:
  - Name (e.g., "Minimal", "Modern")
  - Category (e.g., "minimal", "modern")
  - Preview image URL (or leave blank)
  - Other required fields

### Step 4: Test Brand Section
1. Visit homepage `/`
2. Add customer logos at `/admin/core/customers/`
3. Verify infinite scroll carousel appears

### Step 5: Test Template Carousel
1. Visit homepage `/`
2. Scroll to "قالب های تک و جذاب" section
3. Test carousel:
   - Click left/right buttons
   - Drag with mouse
   - Use arrow keys
   - Observe depth effect and centering

### Step 6: Test Card Builder
1. Click "رایگان شروع کنید" button (or navigate to `/card/builder/`)
2. **Login if prompted** (required)
3. Follow 5-step form:
   - Select template
   - Choose color
   - Fill personal info
   - Add social media
   - Add 2-3 skills
4. Click "ایجاد کارت"

### Step 7: Verify Success Page
1. Should see success message
2. Verify shareable link displays
3. Test QR code:
   - Should display QR code image
   - Should be scannable
   - Should link to card
4. Test copy button
5. Test social sharing buttons
6. Preview card

### Step 8: Test Public Card View
1. From success page, click "نمایش کارت" button
2. Verify public card displays with correct:
   - Theme color (check CSS)
   - All entered information
   - Social links
   - Skills
   - QR code
3. Test action buttons

### Step 9: Verify Theme System
1. Create 2 cards with different colors
2. Visit each public card
3. Verify correct CSS theme is loaded
4. Check page source for correct stylesheet link

### Step 10: Test Admin Interface
1. Visit `/admin/core/usercard/`
2. Verify all cards listed with filters
3. Click on a card to edit
4. Add/remove skills from inline admin
5. Save changes

---

## 🐛 Common Issues & Solutions

### Issue: "Template not found" error
**Solution:** 
- Ensure directory exists: `core/templates/core/`
- Check template file names match exactly
- Verify `APP_DIRS = True` in settings

### Issue: Carousel not moving
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Check if `carousel.js` is loaded (browser console)
- Verify carousel HTML matches class selectors
- Check browser console for JavaScript errors

### Issue: QR code not displaying
**Solution:**
- Verify internet connection (uses external API)
- Check URL is valid and properly encoded
- Try opening API URL directly: `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://example.com`

### Issue: Theme CSS not changing
**Solution:**
- Verify CSS files exist in `static/` folder
- Check color value matches in UserCard model
- Clear static files: `python manage.py collectstatic --clear`
- Check page source to verify correct stylesheet

### Issue: Form won't submit
**Solution:**
- Check browser console for JavaScript errors
- Verify all required fields are filled
- Check CSRF token is present
- Clear form cache and try again

---

## 📊 Database Structure

### UserCard Table:
```
id (PK) | user_id | username | template_id | color | name | email | ... | is_published | created_at
```

### Skill Table:
```
id (PK) | user_card_id | name | created_at
```

---

## 🚀 Performance Tips

1. **Image Optimization:**
   - Use WebP format for preview images
   - Optimize brand logos (under 50KB)
   - Use responsive images

2. **Caching:**
   - Cache template data
   - Cache public card views
   - Use CDN for static files

3. **Database:**
   - Add indexes on frequently searched fields
   - Use select_related for ForeignKey queries
   - Optimize QuerySet usage

4. **Frontend:**
   - Minify CSS and JavaScript
   - Use lazy loading for images
   - Implement pagination for large lists

---

## 🔒 Security Considerations

1. **Authentication:**
   - Only authenticated users can create cards
   - Users can only edit their own cards
   - @login_required decorators applied

2. **Authorization:**
   - Public cards require `is_published=True`
   - Private cards only visible to owner
   - Admin requires superuser status

3. **Input Validation:**
   - Form validation on both client and server
   - XSS protection via template escaping
   - CSRF protection via Django middleware

4. **Data Protection:**
   - Sensitive fields can be made private
   - User data stored securely in database
   - HTTPS recommended for production

---

## 📈 Next Steps

### To Enhance the System:

1. **User Authentication:**
   - Add login/signup pages
   - Email verification
   - Password reset

2. **Advanced Features:**
   - PDF export
   - Analytics dashboard
   - Custom domains
   - Card templates from admin

3. **Performance:**
   - Add caching layer
   - Optimize database queries
   - Implement pagination

4. **Testing:**
   - Write unit tests
   - Add integration tests
   - Performance testing

---

## 📞 Support URLs

| Feature | URL | Status |
|---------|-----|--------|
| Homepage | `/` | ✅ |
| Card Builder | `/card/builder/` | ✅ |
| Success Page | `/card/success/<id>/` | ✅ |
| Public Card | `/card/<username>/` | ✅ |
| Admin | `/admin/` | ✅ |
| API Skills | `/api/skill/add/` | ✅ |

---

## 🎓 Code Examples

### Creating a Card Programmatically:
```python
from django.contrib.auth import get_user_model
from core.models import UserCard, Skill

User = get_user_model()
user = User.objects.get(username='testuser')

card = UserCard.objects.create(
    user=user,
    username='testcard',
    name='Test User',
    short_bio='Test bio',
    email='test@example.com',
    color='blue'
)

Skill.objects.create(user_card=card, name='Python')
Skill.objects.create(user_card=card, name='Django')
```

### Accessing Card Data in Template:
```django
{% if user_card %}
    <h1>{{ user_card.name }}</h1>
    <p>{{ user_card.short_bio }}</p>
    {% for skill in user_card.skills.all %}
        <span>{{ skill.name }}</span>
    {% endfor %}
{% endif %}
```

### Making AJAX Skill Request:
```javascript
fetch('/api/skill/add/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ name: 'New Skill' })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

**Last Updated:** December 5, 2025
**Testing Status:** Ready for QA ✅
**All Features:** Fully Implemented ✅
