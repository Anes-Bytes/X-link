# Monthly/Annual Pricing Implementation - Complete Guide

## Overview
Successfully implemented monthly and annual pricing system for the X-Link Django application. Users can now toggle between monthly and annual plan views via URL parameters (no JavaScript required).

---

## Changes Made

### 1. **Model Update** (`core/models.py`)
Added `period` field to the `Plan` model:

```python
class Plan(models.Model):
    class PeriodChoices(models.TextChoices):
        MONTHLY = "monthly", "ماهانه"
        ANNUAL = "annual", "سالانه"
    
    period = models.CharField(
        max_length=20, 
        choices=PeriodChoices.choices, 
        default="monthly"
    )
```

**Changes:**
- New `period` field with choices: "monthly" or "annual"
- Default value is "monthly"
- Allows filtering plans by subscription period

---

### 2. **Database Migration** (`core/migrations/0006_plan_period.py`)
Created migration file to add the `period` field to the database.

**To apply migration:**
```bash
python manage.py migrate core
```

---

### 3. **View Update** (`core/views.py`)
Updated `landing_view` function to fetch and filter plans by period:

```python
def landing_view(request):
    # ... caching code ...
    
    # Fetch monthly and annual plans separately
    plans_monthly = Plan.objects.filter(period="monthly")...
    plans_annual = Plan.objects.filter(period="annual")...
    
    # Get period from GET parameter (default: monthly)
    period = request.GET.get("period", "monthly")
    active_plans = plans_annual if period == "annual" else plans_monthly
    
    return render(request, "core/landing.html", {
        "plans_monthly": plans_monthly,
        "plans_annual": plans_annual,
        "active_plans": active_plans,
        "current_period": period,
    })
```

**Context Variables:**
- `plans_monthly`: List of monthly plans
- `plans_annual`: List of annual plans
- `current_period`: Current selected period ("monthly" or "annual")

---

### 4. **Template Update** (`core/templates/core/landing.html`)
Redesigned pricing section with period toggle:

#### Period Toggle
```html
<div class="period-toggle">
    <a href="?period=monthly" class="toggle-period-btn {% if current_period != 'annual' %}active{% endif %}">
        <span>ماهانه</span>
    </a>
    <a href="?period=annual" class="toggle-period-btn {% if current_period == 'annual' %}active{% endif %}">
        <span>سالانه</span>
        <span class="discount-label">۲۵٪ تخفیف</span>
    </a>
</div>
```

#### Conditional Rendering
- **Monthly Section**: Renders when `current_period != 'annual'`
- **Annual Section**: Renders when `current_period == 'annual'`
- Shows appropriate price period (`/ماه` or `/سال`)

**Features preserved:**
- All badges, features lists, and buttons remain intact
- Same card layout and styling
- Responsive design maintained

---

### 5. **Styling Updates** (`static/styles.css`)
Added comprehensive CSS for period toggle and responsive behavior:

#### New Classes:
- `.period-toggle`: Toggle container
- `.toggle-period-btn`: Individual toggle button
- `.discount-label`: Discount badge on annual button

#### Responsive Breakpoints:
- **Desktop (1024px+)**: Full 3-column grid
- **Tablet (768px-1023px)**: 2-column layout, stacked toggle
- **Mobile (480px-767px)**: Single column, responsive buttons
- **Small Mobile (<480px)**: Full-width buttons, optimized spacing

---

## Usage Flow

### For Users
1. **Visit Landing Page** → Defaults to monthly plans
2. **Click Annual Button** → Page reloads with `?period=annual`
3. **Click Monthly Button** → Page reloads with `?period=monthly`
4. **View Plans** → See appropriate plans for selected period
5. **Select Plan** → Proceed to payment/signup

### URL Structure
```
# Default (Monthly)
https://xlink.com/
https://xlink.com/?period=monthly

# Annual
https://xlink.com/?period=annual
```

---

## Database Setup

### Create Plans with Period

```python
# Django Shell
from core.models import Plan, Discount, Feature

# Create monthly discount
discount_monthly = Discount.objects.create(value=10)

# Create monthly plan
plan_free_monthly = Plan.objects.create(
    type="Free",
    name="Free Monthly",
    price=0,
    discount=discount_monthly,
    is_special=False,
    period="monthly"
)

# Create annual plan
plan_free_annual = Plan.objects.create(
    type="Free",
    name="Free Annual",
    price=0,
    discount=discount_monthly,
    is_special=False,
    period="annual"
)

# Add features
Feature.objects.create(plan=plan_free_monthly, name="Feature 1")
Feature.objects.create(plan=plan_free_annual, name="Feature 1")
```

### Via Django Admin
1. Go to `/admin/`
2. Navigate to Plan model
3. Edit existing plans and set `period` field
4. Or create new plans with `period` set to "monthly" or "annual"

---

## Cache Management

The view implements caching for performance:

```python
# Cache keys:
- landing_plans_monthly
- landing_plans_annual
- landing_templates
- landing_customers

# Cache timeout: 60 minutes (3600 seconds)
```

### Clear Cache When Updating Plans
```bash
# Django Shell
from django.core.cache import cache
cache.delete_many([
    'landing_plans_monthly',
    'landing_plans_annual',
    'landing_templates',
    'landing_customers'
])
```

---

## Customization Guide

### Change Discount Label
**File**: `core/templates/core/landing.html` (Line ~142)
```html
<span class="discount-label">15٪ تخفیف</span>  <!-- Change percentage -->
```

### Change Toggle Button Text
**File**: `core/templates/core/landing.html` (Line ~136-147)
```html
<span>Monthly</span>  <!-- English example -->
<span>Yearly</span>
```

### Style Toggle Buttons
**File**: `static/styles.css` (Line ~2404+)
```css
.toggle-period-btn {
    /* Customize padding, colors, fonts, etc. */
}
```

### Add More Periods
If adding "quarterly" or other periods:

1. Update Model:
```python
class PeriodChoices(models.TextChoices):
    MONTHLY = "monthly", "ماهانه"
    QUARTERLY = "quarterly", "سه ماهه"
    ANNUAL = "annual", "سالانه"
```

2. Create Migration and apply
3. Update View to fetch quarterly plans
4. Add button in template

---

## Testing Checklist

- [ ] Run migrations: `python manage.py migrate core`
- [ ] Verify Plan model has `period` field
- [ ] Visit landing page → See monthly plans by default
- [ ] Click annual button → Page shows annual plans
- [ ] Click monthly button → Page returns to monthly plans
- [ ] URL changes correctly (check address bar)
- [ ] All cards display properly (desktop, tablet, mobile)
- [ ] Prices show correctly for both periods
- [ ] CTA buttons work correctly
- [ ] Comparison table displays properly
- [ ] Cache works (multiple page loads are fast)

---

## Performance Notes

✅ **Server-side rendering**: No JavaScript overhead
✅ **URL-based routing**: Bookmarkable URLs
✅ **Cached queries**: Efficient database usage
✅ **Responsive CSS**: Mobile-optimized
✅ **SEO-friendly**: Proper URL structure

---

## Troubleshooting

### Plans not showing?
- **Check**: All plans have `period` field set
- **Fix**: Update existing plans: `Plan.objects.all().update(period='monthly')`

### Toggle not working?
- **Check**: View receives GET parameter correctly
- **Debug**: Add `print(request.GET.get("period"))` in view

### Wrong period shows?
- **Check**: `current_period` context variable
- **Fix**: Verify conditional in template: `{% if current_period == 'annual' %}`

### Cache stale?
- **Clear**: `cache.delete_many(['landing_plans_monthly', 'landing_plans_annual'])`
- **Or**: Restart Django development server

---

## Files Modified

1. ✅ `core/models.py` - Added `period` field
2. ✅ `core/views.py` - Updated landing_view function
3. ✅ `core/migrations/0006_plan_period.py` - Database migration
4. ✅ `core/templates/core/landing.html` - Template redesign
5. ✅ `static/styles.css` - Added period toggle styles

---

## Next Steps (Optional)

1. **Add payment integration**: Track monthly vs annual subscriptions
2. **Show savings**: Display annual discount amount in money
3. **Analytics**: Track which period is more popular
4. **Email notifications**: Send period-specific emails
5. **Dashboard**: Show current period subscription in user panel

---

## Support

For issues or questions:
1. Check this documentation
2. Review Django migration docs
3. Check template syntax
4. Verify CSS classes match template

Last Updated: December 16, 2025
