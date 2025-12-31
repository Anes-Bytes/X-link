from django.contrib import admin
from django.db.models import Count

from Billing.models import UserPlan, Discount, Template, Plan, Feature


class FeaturesInline(admin.TabularInline):
    model = Feature
    extra = 0


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('value', 'get_display_name')
    search_fields = ('value',)

    def get_display_name(self, obj):
        return obj.get_value_display()
    get_display_name.short_description = 'نام نمایشی'


@admin.register(Plan)
class PlansAdmin(admin.ModelAdmin):
    """
    Admin interface for Plan model.
    """

    list_display = (
        'name',
        'plan_type',
        'period',
        'get_price_display',
        'get_discounted_price_display',
        'get_savings_display',
        'is_special',
        'is_active',
        'get_features_count'
    )
    list_filter = (
        'plan_type',
        'period',
        'is_special',
        'is_active',
        'discount'
    )
    search_fields = ('name', 'plan_type')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [FeaturesInline]

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('plan_type', 'name', 'period', 'is_active')
        }),
        ('قیمت‌گذاری', {
            'fields': ('price', 'discount', 'is_special')
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('discount').prefetch_related('features')

    def get_price_display(self, obj):
        """Display formatted price."""
        return f"{obj.price:,} تومان"
    get_price_display.short_description = 'قیمت پایه'
    get_price_display.admin_order_field = 'price'

    def get_discounted_price_display(self, obj):
        """Display final price after discount."""
        final_price = obj.get_discounted_price()
        if final_price < obj.price:
            return f"{final_price:,} تومان"
        return "بدون تغییر"
    get_discounted_price_display.short_description = 'قیمت نهایی'

    def get_savings_display(self, obj):
        """Display savings information."""
        if not obj.discount:
            return "بدون تخفیف"

        savings = obj.get_savings_amount()
        percentage = obj.get_savings_percentage()
        return f"{savings:,} تومان ({percentage}%)"
    get_savings_display.short_description = 'تخفیف'

    def get_features_count(self, obj):
        """Display number of features."""
        return obj.features.count()
    get_features_count.short_description = 'تعداد ویژگی‌ها'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', 'get_percentage_display')
    search_fields = ('value',)

    def get_percentage_display(self, obj):
        return f"{obj.value}%"
    get_percentage_display.short_description = 'درصد تخفیف'


@admin.register(Template)
class TemplatesAdmin(admin.ModelAdmin):
    """
    Admin interface for Template model.
    """

    list_display = (
        'name',
        'is_active',
        'delay',
        'get_allowed_plans_display',
        'get_usage_count',
        'created_at'
    )
    list_filter = ('is_active', 'created_at', 'allowed_plans')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'image', 'description', 'is_active')
        }),
        ('پیکربندی', {
            'fields': ('delay', 'allowed_plans')
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'allowed_plans',
            'user_cards'
        ).annotate(
            usage_count=Count('user_cards')
        )

    def get_allowed_plans_display(self, obj):
        """Display allowed plans."""
        plan_values = obj.get_allowed_plan_values()
        if 'all' in plan_values:
            return "همه پلن‌ها"
        return ", ".join(plan_values)
    get_allowed_plans_display.short_description = 'پلن‌های مجاز'

    def get_usage_count(self, obj):
        """Display usage count."""
        return obj.usage_count
    get_usage_count.short_description = 'تعداد کارت استفاده‌کننده'
