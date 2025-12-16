# Services & Portfolio Implementation Guide

## Overview
This implementation adds dynamic **Services** and **Portfolio/Projects** sections to user digital cards. Both sections follow the same pattern as the existing Skills section with full CRUD capabilities.

## Database Models

### Service Model
```python
class Service(models.Model):
    user_card = ForeignKey(UserCard)
    title = CharField(max_length=255)  # Required
    description = CharField(max_length=500)  # Optional
    icon = CharField(max_length=100)  # Font Awesome icon class
    order = IntegerField()  # For ordering
```

### Portfolio Model
```python
class Portfolio(models.Model):
    user_card = ForeignKey(UserCard)
    title = CharField(max_length=255)  # Required
    description = CharField(max_length=500)  # Optional
    image = ImageField(upload_to='portfolio')  # Required
    url = URLField()  # Project link (optional)
    order = IntegerField()  # For ordering
```

## Installation Steps

### 1. Create & Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Register Models in Admin (Optional)
```python
# core/admin.py
from django.contrib import admin
from .models import Service, Portfolio

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_card', 'order', 'created_at')
    list_filter = ('created_at', 'user_card')
    search_fields = ('title', 'user_card__name')
    ordering = ('order',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_card', 'order', 'created_at')
    list_filter = ('created_at', 'user_card')
    search_fields = ('title', 'user_card__name')
    ordering = ('order',)
```

## Frontend Features

### Card Builder (Edit Page)
- **Step 6: Services** - Add/remove/edit services with title, description, icon
- **Step 7: Portfolio** - Add/remove/edit portfolio items with image, title, description, URL
- Dynamic form management with "Add" buttons
- Delete checkboxes for removing items
- Form validation with error messages

### Card View (Public Page)
- **Services Section** - Grid layout with icons, titles, descriptions
- **Portfolio Section** - Image gallery with overlay links
- Responsive grid that adapts to screen size
- Smooth hover animations
- Empty states when no items added

## API Endpoints

### Delete Endpoints
```
DELETE /api/service/<int:service_id>/delete/
DELETE /api/portfolio/<int:portfolio_id>/delete/
```

### Response
```json
{ "success": true }
```

## Form Fields

### Service Form
- **title** (required): Service name
- **description** (optional): Service details
- **icon** (optional): Font Awesome class (e.g., "fas fa-code")
- **order** (optional): Display order

### Portfolio Form
- **title** (required): Project name
- **description** (optional): Project details
- **image** (required): Project screenshot/thumbnail
- **url** (optional): Project link
- **order** (optional): Display order

## CSS Classes

### Service Styling
```css
.services-section       /* Main section container */
.services-container     /* Grid container */
.service-item          /* Individual service card */
.service-title         /* Service name */
.service-description   /* Service description */
.service-content       /* Text content wrapper */
```

### Portfolio Styling
```css
.portfolio-section      /* Main section container */
.portfolio-grid        /* Grid container */
.portfolio-item        /* Individual portfolio card */
.portfolio-thumbnail   /* Image wrapper */
.portfolio-overlay     /* Hover overlay */
.portfolio-link        /* External link button */
.portfolio-title       /* Project name */
.portfolio-description /* Project details */
.portfolio-content     /* Text content wrapper */
```

### Builder Form Styling
```css
.service-form-group    /* Service form wrapper */
.portfolio-form-group  /* Portfolio form wrapper */
.services-container    /* All services container */
.portfolio-container   /* All portfolio items container */
.add-service-btn       /* Add service button */
.add-portfolio-btn     /* Add portfolio button */
.form-row             /* Form fields row */
.form-col             /* Form column */
```

## JavaScript Functionality

### Dynamic Form Management (card_builder.html)
- **addSkillBtn** - Adds new skill forms
- **addServiceBtn** - Adds new service forms
- **addPortfolioBtn** - Adds new portfolio forms

Each button:
1. Clones the first form element
2. Updates all form field names with new index
3. Clears field values
4. Increments TOTAL_FORMS counter

### Example Usage
```javascript
// Services formset management
const addServiceBtn = document.getElementById('addServiceBtn');
addServiceBtn.addEventListener('click', function(e) {
    // Adds new service form dynamically
});
```

## View Logic

### card_builder_view()
Handles POST requests with 4 formsets:
1. UserCardForm (main card info)
2. SkillInlineFormSet
3. ServiceInlineFormSet ← New
4. PortfolioInlineFormSet ← New

All formsets are validated and saved together.

### view_card()
Public view with prefetch_related:
```python
UserCard.objects.prefetch_related(
    "skills", 
    "services",        # ← New
    "portfolio_items"  # ← New
)
```

## Responsive Breakpoints

### Services Grid
- **Desktop** (1200px+): 3-4 columns
- **Tablet** (768-1200px): 2-3 columns  
- **Mobile** (480-768px): 1-2 columns
- **Small Phone** (<480px): 1 column

### Portfolio Grid
- **Desktop** (1200px+): 3-4 columns
- **Tablet** (768-1200px): 2-3 columns
- **Mobile** (480-768px): 1-2 columns
- **Small Phone** (<480px): 1 column

## Customization

### Change Service Icon
Default icon is "fas fa-star". Customize in card_view.html:
```django-html
{% if service.icon %}
    <i class="{{ service.icon }}"></i>
{% else %}
    <i class="fas fa-star"></i>  <!-- Change this -->
{% endif %}
```

### Change Portfolio Image Ratio
In services-portfolio.css:
```css
.portfolio-thumbnail {
    aspect-ratio: 16 / 10;  /* Change to 16/9, 4/3, etc. */
}
```

### Adjust Grid Columns
In services-portfolio.css:
```css
.services-container {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    /* Increase minmax value for fewer columns */
}

.portfolio-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    /* Increase minmax value for fewer columns */
}
```

## Testing

### 1. Add Services
- Navigate to card builder
- Add 3-5 services with titles and icons
- Save card
- View public card and verify display

### 2. Add Portfolio Items
- Add 2-3 portfolio items with images
- Add URLs to some items
- Save card
- Check hover effects and link functionality

### 3. Responsive Testing
- Test on desktop, tablet, mobile
- Verify grid adapts properly
- Check overlay animations on portfolio

### 4. Form Validation
- Try submitting empty required fields
- Verify error messages display
- Check image upload validation

## Files Modified

1. **core/models.py** - Added Service and Portfolio models
2. **core/forms.py** - Added forms and formsets
3. **core/views.py** - Updated views and added formsets
4. **core/urls.py** - Added new API endpoints
5. **core/templates/core/card_builder.html** - Added form sections and JS
6. **core/templates/core/card_view.html** - Added dynamic sections
7. **templates/_base.html** - Added CSS link
8. **static/services-portfolio.css** - New styling file

## Performance Notes

- Images are prefetched in views for better performance
- Portfolio images should be optimized (max 800x600px)
- Use lazy loading for images in production
- Cache query results for frequently accessed cards

## Security

- All delete endpoints require login (`@login_required`)
- CSRF protection via `{% csrf_token %}`
- User can only edit/delete their own items
- URL validation on portfolio links
- Image upload validation (type & size)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android)

## Troubleshooting

### Forms not saving
- Check CSRF token in form
- Verify all formsets validate correctly
- Check database for constraint violations

### Portfolio images not showing
- Verify MEDIA_URL and MEDIA_ROOT configured
- Check image upload permissions
- Test with small image file

### Dynamic forms not adding
- Open browser console for errors
- Check formset prefix in forms
- Verify TOTAL_FORMS increment logic

### Styling issues
- Clear browser cache
- Verify CSS file linked in template
- Check CSS class names match HTML

## Next Steps

1. Add ordering/drag-drop functionality
2. Implement service pricing display
3. Add portfolio filters/categories
4. Integrate with analytics
5. Add bulk import from CSV
6. Implement service/portfolio templates
