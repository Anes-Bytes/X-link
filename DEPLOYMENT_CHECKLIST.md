# Services & Portfolio - Deployment Checklist

## Pre-Deployment

- [ ] All files modified as per guide
- [ ] Migrations created and tested locally
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] CSS file added to static folder
- [ ] Template links verified
- [ ] No syntax errors in Python/JavaScript/CSS

## Database Migration

```bash
# Create migrations
python manage.py makemigrations

# Review migration file
# Then apply
python manage.py migrate
```

## Code Review

- [ ] Models have proper Meta classes
- [ ] Form fields validated
- [ ] View logic handles all formsets correctly
- [ ] URL patterns registered
- [ ] AJAX endpoints respond properly
- [ ] CSS classes match templates

## Testing Checklist

### Functionality
- [ ] Add service - form renders, saves, displays
- [ ] Edit service - loads existing data, saves changes
- [ ] Delete service - removes from database and display
- [ ] Add portfolio item - form renders, image uploads, saves
- [ ] Edit portfolio - loads image, saves changes
- [ ] Delete portfolio - removes from database

### Responsive Design
- [ ] Desktop (1920px) - 3-4 columns
- [ ] Laptop (1366px) - 2-3 columns
- [ ] Tablet (768px) - 2-3 columns
- [ ] Mobile (375px) - 1-2 columns
- [ ] Small phone (320px) - 1 column

### Forms
- [ ] Required field validation works
- [ ] Error messages display
- [ ] Max length validation works
- [ ] Image validation works
- [ ] URL validation works
- [ ] Multiple forms can be added

### Public Display
- [ ] Services render with icons
- [ ] Portfolio items display images
- [ ] Hover effects work smoothly
- [ ] Links open in new tab
- [ ] Responsive on all devices
- [ ] Performance acceptable (images load fast)

### Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

## Performance Checks

- [ ] Query optimization (prefetch_related used)
- [ ] CSS is minified
- [ ] JavaScript works without errors
- [ ] No console warnings/errors
- [ ] Page load time acceptable
- [ ] Images optimized

## Security Checks

- [ ] CSRF protection active
- [ ] User can only edit own card
- [ ] Delete endpoints require login
- [ ] File upload validated
- [ ] URLs validated
- [ ] No SQL injection possible
- [ ] No XSS vulnerabilities

## Deployment Steps

1. **Backup Database**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Test Locally**
   ```bash
   python manage.py runserver
   ```

5. **Deploy to Production**
   - Push changes to repo
   - Run migrations on production
   - Clear cache if applicable
   - Monitor error logs

## Post-Deployment

- [ ] Verify migrations applied successfully
- [ ] Test add/edit/delete on production
- [ ] Check responsive design in production
- [ ] Verify CSS loads correctly
- [ ] Monitor error logs for issues
- [ ] Test AJAX endpoints
- [ ] Verify images display correctly
- [ ] Check mobile performance

## Rollback Plan

If issues occur:
```bash
# Rollback migration
python manage.py migrate core 0004_previous_migration

# Restore database
python manage.py loaddata backup.json
```

## Monitoring

After deployment, monitor:
- [ ] Error logs for exceptions
- [ ] Database query performance
- [ ] File storage usage
- [ ] User feedback for UX issues
- [ ] Load times on mobile
- [ ] Image optimization effectiveness

## Documentation

- [ ] README updated with new features
- [ ] API documentation created
- [ ] User guide created
- [ ] Admin documentation created
- [ ] Known issues documented
- [ ] Future improvements listed

## Success Criteria

✅ All CRUD operations work
✅ Responsive on all devices
✅ No errors in console/logs
✅ Fast page load times
✅ Professional appearance
✅ User feedback positive

## Quick Links

- Models: [core/models.py](core/models.py)
- Forms: [core/forms.py](core/forms.py)
- Views: [core/views.py](core/views.py)
- URLs: [core/urls.py](core/urls.py)
- Templates: [core/templates/core/](core/templates/core/)
- CSS: [static/services-portfolio.css](static/services-portfolio.css)

## Support

For issues:
1. Check error logs
2. Review SERVICES_PORTFOLIO_GUIDE.md
3. Test in local environment
4. Check browser console
5. Verify migrations applied

---

**Version**: 1.0  
**Last Updated**: December 15, 2025  
**Status**: Ready for Production
