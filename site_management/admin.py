from django.contrib import admin

from .models import SiteContext, Customer, Banners


@admin.register(SiteContext)
class SiteContextAdmin(admin.ModelAdmin):
    """
    Admin interface for site-wide configuration.
    """

    list_display = ('site_name', 'created_at', 'updated_at')
    search_fields = ('site_name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('site_name', 'logo')
        }),
        ('محتوای قهرمان', {
            'fields': (
                'hero_section_text_part1',
                'hero_section_text_part2',
                'hero_section_text_description'
            ),
            'classes': ('collapse',)
        }),
        ('فوتر', {
            'fields': ('footer_section_text_part1',),
            'classes': ('collapse',)
        }),
        ('شبکه‌های اجتماعی', {
            'fields': (
                ('footer_telegram_url', 'footer_linkedin_url'),
                ('footer_github_url', 'footer_instagram_url'),
            ),
            'classes': ('collapse',)
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Limit to one site context."""
        return not SiteContext.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site context."""
        return False


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for customer testimonials/logos.
    """

    list_display = (
        'company_name',
        'company_url',
        'is_active',
        'display_order',
        'get_site_context'
    )
    list_filter = ('is_active', 'site_context', 'created_at')
    search_fields = ('company_name', 'company_url')
    readonly_fields = ('created_at',)
    list_editable = ('is_active', 'display_order')

    fieldsets = (
        ('اطلاعات شرکت', {
            'fields': ('company_name', 'company_url',)
        }),
        ('پیکربندی', {
            'fields': ('site_context', 'is_active', 'display_order')
        }),
        ('تاریخچه', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('site_context')

    def get_site_context(self, obj):
        """Display site context name."""
        return obj.site_context.site_name
    get_site_context.short_description = 'سایت'
    get_site_context.admin_order_field = 'site_context__site_name'


@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    """
    Admin interface for banner management.
    """

    list_display = ('title', 'description', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'description')

    fieldsets = (
        ('محتوا', {
            'fields': ('title', 'description')
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
