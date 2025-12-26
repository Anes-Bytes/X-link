from django.contrib import admin
from django.db.models import Prefetch

from Billing.models import UserPlan
from cards.models import UserCard, Skill, Service, Portfolio
# ========== Inline ADMINS ==========

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


class PortfolioInline(admin.TabularInline):
    model = Portfolio
    extra = 0

# ========== MAIN ADMINS ==========


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'get_user_full_name', 'get_user_plans', 'color', 'is_published', 'get_views_count', 'created_at')
    list_filter = ('color', 'is_published', 'created_at', 'user__plan')
    search_fields = ('name', 'username', 'user__username', 'user__email', 'user__full_name')
    readonly_fields = ('created_at', 'updated_at', 'views')
    inlines = [SkillInline, ServiceInline, PortfolioInline]
    raw_id_fields = ('user',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'template'
        ).prefetch_related(
            'skills',
            'services',
            'portfolio_items',
            Prefetch('user__plan', queryset=UserPlan.objects.all())
        )

    def get_user_full_name(self, obj):
        return obj.user.full_name if obj.user.full_name else obj.user.phone
    get_user_full_name.short_description = 'کاربر'
    get_user_full_name.admin_order_field = 'user__full_name'

    def get_user_plans(self, obj):
        plans = obj.user.plan.all()
        if plans:
            return ", ".join([plan.get_value_display() for plan in plans])
        return "بدون پلن"
    get_user_plans.short_description = 'پلن‌ها'
    get_user_plans.admin_order_field = 'user__plan__value'

    def get_views_count(self, obj):
        return f"{obj.views:,}"
    get_views_count.short_description = 'بازدیدها'

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'username', "profile_picture",'template', "black_background", "blue_tick", "stars_background", 'views', 'show_views')
        }),
        ('Personal Information', {
            'fields': ('name', 'short_bio', 'description', 'email', 'website')
        }),
        ('Social Media', {
            'fields': (
                'instagram_username',
                'telegram_username',
                'linkedin_username',
                'github_username',
                'youtube_username',
                'twitter_username',
            )
        }),
        ('Styling', {
            'fields': ('color',)
        }),
        ('Status', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )

