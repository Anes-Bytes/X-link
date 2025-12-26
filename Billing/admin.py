from django.contrib import admin
from django.db.models import Count

from Billing.models import UserPlan, Discount, Template

@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('value', 'get_display_name')
    search_fields = ('value',)

    def get_display_name(self, obj):
        return obj.get_value_display()
    get_display_name.short_description = 'نام نمایشی'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', 'get_percentage_display')
    search_fields = ('value',)

    def get_percentage_display(self, obj):
        return f"{obj.value}%"
    get_percentage_display.short_description = 'درصد تخفیف'


@admin.register(Template)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'delay', 'only_for_premium', 'is_active', 'get_allowed_plans', 'get_usage_count')
    list_filter = ('only_for_premium', 'is_active', 'allowed_plans')
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'allowed_plans',
            'user_cards'
        ).annotate(
            usage_count=Count('user_cards')
        )

    def get_allowed_plans(self, obj):
        plans = obj.allowed_plans.all()
        if plans:
            return ", ".join([plan.get_value_display() for plan in plans])
        return "همه پلن‌ها"
    get_allowed_plans.short_description = 'پلن‌های مجاز'

    def get_usage_count(self, obj):
        return obj.usage_count
    get_usage_count.short_description = 'تعداد استفاده'
