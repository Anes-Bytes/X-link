# Services & Portfolio - Code Reference

## Quick Copy-Paste Code Snippets

### 1. Admin Registration (Optional)

Add this to `core/admin.py`:

```python
from django.contrib import admin
from .models import Service, Portfolio

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_card', 'order', 'created_at')
    list_filter = ('created_at', 'user_card')
    search_fields = ('title', 'user_card__name')
    ordering = ('order',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('user_card', 'title', 'description')
        }),
        ('Display', {
            'fields': ('icon', 'order')
        }),
    )


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_card', 'order', 'created_at')
    list_filter = ('created_at', 'user_card')
    search_fields = ('title', 'user_card__name')
    ordering = ('order',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('user_card', 'title', 'description')
        }),
        ('Media', {
            'fields': ('image', 'url')
        }),
        ('Display', {
            'fields': ('order',)
        }),
    )
```

### 2. Custom CSS Themes

To create a themed version (e.g., `services-portfolio-dark.css`):

```css
/* Dark Theme Variables */
:root {
    --primary-blue: #1e40af;
    --cyan-neon: #06b6d4;
    --text-white: #f0f9ff;
    --text-gray: #94a3b8;
    --bg-dark: #0f172a;
    --surface-darker: #1e293b;
    --border-light: rgba(30, 64, 175, 0.2);
    --border-hover: rgba(6, 182, 212, 0.4);
}

/* Then override specific classes as needed */
.service-item {
    background: linear-gradient(135deg, 
        rgba(30, 64, 175, 0.08), 
        rgba(6, 182, 212, 0.05));
}
```

### 3. Service with Ordering

To display services in custom order:

```django-html
<!-- In card_view.html -->
<div class="services-container">
    {% regroup user_card.services.all by order as services_by_order %}
    {% for group in services_by_order %}
        {% for service in group.list %}
        <div class="service-item">
            <i class="{{ service.icon }}"></i>
            <div class="service-content">
                <h4>{{ service.title }}</h4>
                <p>{{ service.description }}</p>
            </div>
        </div>
        {% endfor %}
    {% endfor %}
</div>
```

### 4. Portfolio with Filtering

To add category filtering:

```python
# In models.py - Add to Portfolio
class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App'),
        ('design', 'UI/UX Design'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    # ... rest of model
```

Then in template:

```django-html
<!-- Category filter buttons -->
<div class="portfolio-filters">
    <button class="filter-btn active" data-filter="all">All</button>
    {% for category, label in portfolio_categories %}
    <button class="filter-btn" data-filter="{{ category }}">{{ label }}</button>
    {% endfor %}
</div>

<div class="portfolio-grid" id="portfolioGrid">
    {% for portfolio in user_card.portfolio_items.all %}
    <div class="portfolio-item" data-category="{{ portfolio.category }}">
        <!-- ... -->
    </div>
    {% endfor %}
</div>

<script>
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const filter = this.dataset.filter;
        document.querySelectorAll('.portfolio-item').forEach(item => {
            if (filter === 'all' || item.dataset.category === filter) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});
</script>
```

### 5. Service Pricing Display

To add pricing to services:

```python
# In models.py - Add to Service
class Service(models.Model):
    # ... existing fields
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
```

In template:

```django-html
<div class="service-item">
    <i class="{{ service.icon }}"></i>
    <div class="service-content">
        <div class="service-header">
            <h4>{{ service.title }}</h4>
            {% if service.price %}
            <span class="service-price">${{ service.price }}</span>
            {% endif %}
        </div>
        <p>{{ service.description }}</p>
    </div>
</div>
```

### 6. Portfolio Statistics

To add view count to portfolio:

```python
# In models.py - Add to Portfolio
class Portfolio(models.Model):
    # ... existing fields
    views = models.IntegerField(default=0)
```

In view:

```python
def view_card(request, username):
    user_card = get_object_or_404(
        UserCard.objects.prefetch_related("portfolio_items"),
        username=username
    )
    
    # Track portfolio views
    portfolio_id = request.GET.get('portfolio_id')
    if portfolio_id:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        portfolio.views += 1
        portfolio.save()
    
    return render(request, 'core/card_view.html', {'user_card': user_card})
```

### 7. Batch Delete Services

Add to views.py:

```python
@require_http_methods(["POST"])
@login_required
def delete_all_services_ajax(request):
    """Delete all services for user card"""
    try:
        user_card = UserCard.objects.get(user=request.user)
        user_card.services.all().delete()
        return JsonResponse({'success': True, 'count': 0})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

Add to urls.py:

```python
path('api/services/delete-all/', views.delete_all_services_ajax, name='delete_all_services_ajax'),
```

### 8. Export Services to JSON

Add to views.py:

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
@login_required
def export_services_json(request):
    """Export user's services as JSON"""
    try:
        user_card = UserCard.objects.get(user=request.user)
        services = user_card.services.values_list('title', 'description', 'icon', 'order')
        
        return JsonResponse({
            'success': True,
            'services': [
                {
                    'title': s[0],
                    'description': s[1],
                    'icon': s[2],
                    'order': s[3],
                }
                for s in services
            ]
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### 9. Custom Form Rendering

In `card_builder.html`:

```django-html
<!-- Custom rendering for single service form -->
<div class="service-card">
    <div class="service-form-grid">
        <div class="form-field">
            <label>Service Name *</label>
            {{ service_form.title }}
        </div>
        <div class="form-field">
            <label>Icon (Font Awesome)</label>
            {{ service_form.icon }}
            <small>e.g., "fas fa-code" or "fab fa-react"</small>
        </div>
        <div class="form-field full-width">
            <label>Description</label>
            {{ service_form.description }}
        </div>
    </div>
</div>
```

CSS:

```css
.service-card {
    padding: 20px;
    background: rgba(58, 134, 255, 0.05);
    border-radius: 8px;
    border: 1px solid rgba(58, 134, 255, 0.2);
}

.service-form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.form-field.full-width {
    grid-column: 1 / -1;
}

.form-field label {
    display: block;
    margin-bottom: 6px;
    color: #fff;
    font-weight: 600;
}

.form-field small {
    display: block;
    margin-top: 4px;
    color: #a5b4d0;
    font-size: 0.85rem;
}
```

### 10. Service Search/Filter

Add to card_view.html:

```django-html
<!-- Search/filter services -->
<div class="services-header">
    <h3>Services</h3>
    <input type="text" 
           id="serviceSearch" 
           class="service-search" 
           placeholder="Search services...">
</div>

<script>
const searchInput = document.getElementById('serviceSearch');
const serviceItems = document.querySelectorAll('.service-item');

searchInput.addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    
    serviceItems.forEach(item => {
        const title = item.querySelector('.service-title').textContent.toLowerCase();
        const description = item.querySelector('.service-description').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});
</script>

<style>
.service-search {
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(58, 134, 255, 0.3);
    border-radius: 6px;
    color: #fff;
    font-size: 0.95rem;
    width: 100%;
    max-width: 300px;
    margin-left: auto;
}

.service-search::placeholder {
    color: rgba(165, 180, 208, 0.6);
}

.service-search:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.12);
    border-color: #00f6ff;
    box-shadow: 0 0 12px rgba(0, 246, 255, 0.25);
}
</style>
```

### 11. Portfolio Image Optimization

Add to forms.py:

```python
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class PortfolioForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Optimize image
            img = Image.open(image)
            
            # Resize if too large
            max_size = (800, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Compress and save
            img_io = BytesIO()
            img.save(img_io, format='WEBP', quality=85)
            img_io.seek(0)
            
            image = ContentFile(img_io.getvalue(), name=f"{image.name}.webp")
        
        return image
```

### 12. Signal for Auto-Ordering

Add to models.py:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Service)
def auto_order_service(sender, instance, created, **kwargs):
    if created and instance.order == 0:
        max_order = Service.objects.filter(
            user_card=instance.user_card
        ).aggregate(models.Max('order'))['order__max'] or 0
        instance.order = max_order + 1
        instance.save()

@receiver(post_save, sender=Portfolio)
def auto_order_portfolio(sender, instance, created, **kwargs):
    if created and instance.order == 0:
        max_order = Portfolio.objects.filter(
            user_card=instance.user_card
        ).aggregate(models.Max('order'))['order__max'] or 0
        instance.order = max_order + 1
        instance.save()
```

---

## Font Awesome Icon Examples

Popular service icons:

```
Web Development:    fas fa-code
Mobile Apps:        fas fa-mobile-alt
UI/UX Design:       fas fa-paint-brush
Consulting:         fas fa-chart-line
Photography:        fas fa-camera
Copywriting:        fas fa-pen-fancy
Social Media:       fas fa-share-alt
Marketing:          fas fa-bullhorn
Branding:           fas fa-palette
Animation:          fas fa-film
Database:           fas fa-database
Cloud:              fas fa-cloud
Security:           fas fa-shield-alt
Testing:            fas fa-flask
Deployment:         fas fa-rocket
Support:            fas fa-headset
```

---

## Useful Django Queries

```python
# Get user's services
user_services = Service.objects.filter(user_card__user=request.user)

# Get services ordered by order field
services = user_card.services.order_by('order')

# Count services
service_count = user_card.services.count()

# Delete all services
user_card.services.all().delete()

# Get portfolio by URL
portfolio = Portfolio.objects.filter(url__isnull=False)

# Count portfolio items
portfolio_count = user_card.portfolio_items.count()

# Get most viewed portfolio
top_portfolio = Portfolio.objects.order_by('-views')[:5]
```

---

This document provides quick copy-paste solutions for common customizations and extensions.
