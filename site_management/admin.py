from django.contrib import admin

from .models import SiteContext, Customers, Banners


@admin.register(SiteContext)
class SiteContextAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    search_fields = ('site_name',)


@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title', 'description')


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_url', 'get_site_context')
    search_fields = ('company_name', 'company_url')
    list_filter = ('SiteContext',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('SiteContext')

    def get_site_context(self, obj):
        return obj.SiteContext.site_name
    get_site_context.short_description = 'سایت'
    get_site_context.admin_order_field = 'SiteContext__site_name'