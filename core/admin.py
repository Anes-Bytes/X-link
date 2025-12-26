from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Prefetch, Count, Q

from .models import CustomUser, Customers, Template, SiteContext, Plan, Discount, Feature, UserCard, Skill, Service, Portfolio, Banners, \
    UserMessages, UserPlan, OTP


# ========== Inline ADMINS ==========
class FeaturesInline(admin.TabularInline):
    model = Feature
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


class PortfolioInline(admin.TabularInline):
    model = Portfolio
    extra = 1


class UserMessagesInline(admin.TabularInline):
    model = UserMessages
    extra = 1


class OTPInline(admin.TabularInline):
    model = OTP
    extra = 0
    readonly_fields = ('code', 'created_at', 'expires_at')
    can_delete = False


# ========== MAIN ADMINS ==========

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


@admin.register(Plan)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'period', 'price', 'get_final_price', 'is_special', 'get_discount_percentage')
    list_filter = ('type', 'period', 'is_special', 'discount')
    search_fields = ('name', 'type')
    inlines = [FeaturesInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('discount').prefetch_related('Features')

    def get_final_price(self, obj):
        return f"{obj.get_final_price():,}"
    get_final_price.short_description = 'قیمت نهایی'

    def get_discount_percentage(self, obj):
        if obj.discount:
            return f"{obj.discount.value}%"
        return "بدون تخفیف"
    get_discount_percentage.short_description = 'تخفیف'
    get_discount_percentage.admin_order_field = 'discount__value'


@admin.register(SiteContext)
class SiteContextAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    search_fields = ('site_name',)


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


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('phone', 'full_name', 'email', 'get_plans_display', 'plan_expires', 'is_staff', 'is_active', 'date_joined', 'created_at', 'updated_at')
    readonly_fields = ["created_at", "updated_at"]
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'plan', 'date_joined')
    ordering = ('-date_joined',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'plan',
            'messages',
            'otps',
            Prefetch('user_card', queryset=UserCard.objects.select_related('template'))
        ).annotate(
            messages_count=Count('messages'),
            cards_count=Count('user_card')
        )

    def get_plans_display(self, obj):
        plans = obj.plan.all()
        if plans:
            return ", ".join([plan.get_value_display() for plan in plans])
        return "بدون پلن"
    get_plans_display.short_description = 'پلن‌ها'
    get_plans_display.admin_order_field = 'plan__value'

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', "plan", "plan_expires_at")}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'username', "plan", "plan_expires_at")}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    search_fields = ('phone', 'full_name', 'email', 'username')
    inlines = [
        UserMessagesInline,
        OTPInline,
    ]



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', 'get_percentage_display')
    search_fields = ('value',)

    def get_percentage_display(self, obj):
        return f"{obj.value}%"
    get_percentage_display.short_description = 'درصد تخفیف'


@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title', 'description')


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('value', 'get_display_name')
    search_fields = ('value',)

    def get_display_name(self, obj):
        return obj.get_value_display()
    get_display_name.short_description = 'نام نمایشی'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user_card_name', 'created_at')
    search_fields = ('title', 'user_card__name', 'user_card__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_card')

    def get_user_card_name(self, obj):
        return obj.user_card.name
    get_user_card_name.short_description = 'کارت کاربر'
    get_user_card_name.admin_order_field = 'user_card__name'


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user_card_name', 'url', 'created_at')
    search_fields = ('title', 'user_card__name', 'user_card__username', 'url')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_card')

    def get_user_card_name(self, obj):
        return obj.user_card.name
    get_user_card_name.short_description = 'کارت کاربر'
    get_user_card_name.admin_order_field = 'user_card__name'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_card_name', 'created_at')
    search_fields = ('name', 'user_card__name', 'user_card__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_card')

    def get_user_card_name(self, obj):
        return obj.user_card.name
    get_user_card_name.short_description = 'کارت کاربر'
    get_user_card_name.admin_order_field = 'user_card__name'


@admin.register(UserMessages)
class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'text', 'url', 'created_at')
    search_fields = ('user__full_name', 'user__phone', 'text', 'url')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.phone
    get_user_name.short_description = 'کاربر'
    get_user_name.admin_order_field = 'user__full_name'


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'code', 'created_at', 'expires_at', 'is_expired')
    search_fields = ('user__full_name', 'user__phone', 'code')
    list_filter = ('created_at', 'expires_at')
    readonly_fields = ('code', 'created_at', 'expires_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.phone
    get_user_name.short_description = 'کاربر'
    get_user_name.admin_order_field = 'user__full_name'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False