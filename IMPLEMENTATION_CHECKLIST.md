# Monthly/Annual Pricing - Implementation Checklist

## ✅ Completed Tasks

### Model Changes
- [x] Added `period` field to Plan model
- [x] Created PeriodChoices (MONTHLY, ANNUAL)
- [x] Set default period to "monthly"

### Database Migration
- [x] Created migration file: `0006_plan_period.py`
- [x] Migration is ready to be applied

### View Logic
- [x] Updated `landing_view()` function
- [x] Fetch plans separately by period
- [x] Get period from GET parameter
- [x] Pass all context variables

### Template
- [x] Replaced button toggle with link toggle
- [x] Added `.period-toggle` container
- [x] Conditional rendering for monthly/annual sections
- [x] Updated price period display (`/ماه` vs `/سال`)
- [x] Preserved all badges, features, and buttons
- [x] Maintained responsive design

### Styling
- [x] Added `.period-toggle` styles
- [x] Added `.toggle-period-btn` styles
- [x] Added `.discount-label` styles
- [x] Updated responsive breakpoints
- [x] Mobile optimization for toggle buttons

---

## 📋 Next Steps to Deploy

### 1. Apply Database Migration
```bash
python manage.py makemigrations
python manage.py migrate core
```

### 2. Set Up Plans in Database
```bash
# Option A: Django Admin (/admin/)
# Edit existing plans and set period field

# Option B: Django Shell
python manage.py shell
# Then create/update plans with period field
```

### 3. Test the Implementation
```bash
# Start development server
python manage.py runserver

# Visit:
# - http://localhost:8000/ (monthly)
# - http://localhost:8000/?period=annual (annual)
```

### 4. Verify Functionality
- [ ] Visit landing page
- [ ] Verify monthly plans show by default
- [ ] Click annual button
- [ ] Verify annual plans show
- [ ] Click monthly button
- [ ] Verify monthly plans return
- [ ] Test on mobile devices
- [ ] Verify cache works

---

## 📝 Important Notes

### No JavaScript Required
- Uses server-side rendering (Django template)
- URLs are bookmarkable
- Works with JavaScript disabled
- Better for SEO

### Backward Compatibility
- Existing plans default to "monthly"
- No data loss
- Old URLs still work

### Cache Considerations
- Cache is set to 1 hour (3600 seconds)
- Clear cache if plans updated in admin:
  ```python
  from django.core.cache import cache
  cache.delete('landing_plans_monthly')
  cache.delete('landing_plans_annual')
  ```

---

## 🔧 Quick Configuration Reference

### Change Default Period
**File**: `core/views.py` (Line ~119)
```python
period = request.GET.get("period", "monthly")  # "monthly" is default
```

### Change Discount Percentage Text
**File**: `core/templates/core/landing.html` (Line ~142)
```html
<span class="discount-label">۲۵٪ تخفیف</span>
```

### Change Toggle Button Labels
**File**: `core/templates/core/landing.html` (Line ~136-147)
```html
<span>ماهانه</span>  <!-- Monthly in Farsi -->
<span>سالانه</span>  <!-- Annual in Farsi -->
```

---

## 🚀 After Deployment

### Monitor
1. Check page load times (caching working?)
2. Verify toggle clicks are working
3. Monitor database queries (should be cached)

### Maintain
1. Update plans via Django admin when needed
2. Clear cache if changes don't show
3. Respond to user feedback

### Future Enhancements
1. Add analytics tracking for period selection
2. Show monetary savings for annual plans
3. Add comparison table for periods
4. Email notifications for period-specific offers

---

## ❓ FAQ

**Q: Do I need to update existing plans?**
A: No. All existing plans default to "monthly" via migration.

**Q: Can users see both monthly and annual plans together?**
A: No. Template shows one or the other based on the `?period=` parameter.

**Q: What if a user doesn't click the toggle?**
A: They see monthly plans by default (default behavior).

**Q: Will this affect existing plan URLs?**
A: No. The view handles both cases gracefully.

**Q: How do I add more periods (e.g., quarterly)?**
A: Update the PeriodChoices in the model, create migration, update view and template.

---

## 📞 Support Commands

```bash
# Check current plans in database
python manage.py shell
>>> from core.models import Plan
>>> Plan.objects.all().values('type', 'period', 'price')

# Update all plans to monthly (if needed)
>>> Plan.objects.all().update(period='monthly')

# Clear cache
>>> from django.core.cache import cache
>>> cache.clear()

# Run migrations
python manage.py migrate core

# Check migration status
python manage.py showmigrations core
```

---

## 📚 Files Changed Summary

| File | Changes |
|------|---------|
| `core/models.py` | Added `period` field to Plan model |
| `core/views.py` | Updated landing_view to fetch plans by period |
| `core/migrations/0006_plan_period.py` | New migration file |
| `core/templates/core/landing.html` | Replaced button toggle with link toggle |
| `static/styles.css` | Added period toggle styling |

---

**Status**: ✅ Ready for deployment
**Last Updated**: December 16, 2025
**Version**: 1.0
