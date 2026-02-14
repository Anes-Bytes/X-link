from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html

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
    """
    Admin interface for UserCard model with comprehensive management.
    """

    list_display = (
        'name',
        'username',
        'get_user_display',
        'get_user_plans',
        'color',
        'is_published',
        'get_views_display',
        'get_card_url_link',
        'created_at'
    )
    list_filter = (
        'color',
        'is_published',
        'template',
        'created_at',
        'user__plan__value'
    )
    search_fields = (
        'name',
        'username',
        'user__full_name',
        'user__phone',
        'user__email'
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'views',
        'get_card_url_link'
    )
    raw_id_fields = ('user',)
    inlines = [SkillInline, ServiceInline, PortfolioInline]

    actions = ['publish_cards', 'unpublish_cards', 'reset_view_counts']

    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'name', 'username', 'profile_picture'),
            'classes': ('wide',)
        }),
        ('محتوا', {
            'fields': ('short_bio', 'description', 'phone_number', 'email', 'website'),
            'classes': ('wide',)
        }),
        ('شبکه‌های اجتماعی', {
            'fields': (
                ('instagram_username', 'telegram_username'),
                ('linkedin_username', 'github_username'),
                ('youtube_username', 'twitter_username'),
            ),
            'classes': ('collapse',)
        }),
        ('طراحی و قالب', {
            'fields': ('template', 'color'),
            'classes': ('wide',)
        }),
        ('ویژگی‌های ویژه', {
            'fields': ('blue_tick', 'stars_background', 'black_background'),
            'classes': ('collapse',)
        }),
        ('آمار و وضعیت', {
            'fields': ('views', 'show_views', 'is_published', 'get_card_url_link'),
            'classes': ('wide',)
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'template'
        ).prefetch_related(
            'skills',
            'services',
            'portfolio_items',
            'user__plan'
        )

    def get_user_display(self, obj):
        """Display user information."""
        user = obj.user
        return f"{user.full_name or 'بدون نام'} ({user.phone})"
    get_user_display.short_description = 'کاربر'
    get_user_display.admin_order_field = 'user__full_name'

    def get_user_plans(self, obj):
        """Display user's active plans."""
        plans = obj.user.get_active_plans()
        if plans:
            return ", ".join(plans)
        return "بدون پلن"
    get_user_plans.short_description = 'پلن‌های فعال'

    def get_views_display(self, obj):
        """Display formatted view count."""
        return f"{obj.views:,}"
    get_views_display.short_description = 'بازدیدها'
    get_views_display.admin_order_field = 'views'

    def get_card_url_link(self, obj):
        """Display clickable link to the card."""
        url = obj.get_card_url()
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
    get_card_url_link.short_description = 'لینک کارت'

    # Actions
    def publish_cards(self, request, queryset):
        """Publish selected cards."""
        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            f'{updated} کارت منتشر شدند.',
            level='SUCCESS'
        )
    publish_cards.short_description = 'انتشار کارت‌های انتخاب شده'

    def unpublish_cards(self, request, queryset):
        """Unpublish selected cards."""
        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            f'{updated} کارت از انتشار خارج شدند.',
            level='SUCCESS'
        )
    unpublish_cards.short_description = 'لغو انتشار کارت‌های انتخاب شده'

    def reset_view_counts(self, request, queryset):
        """Reset view counts for selected cards."""
        updated = queryset.update(views=0)
        self.message_user(
            request,
            f'آمار بازدید {updated} کارت ریست شد.',
            level='SUCCESS'
        )
    reset_view_counts.short_description = 'ریست آمار بازدید'

