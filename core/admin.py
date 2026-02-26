from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Prefetch, Count

from cards.models import UserCard
from .models import CustomUser, OTP, UserSubdomain
from .forms import CustomUserChangeForm


# ========== Inline ADMINS ==========

class OTPInline(admin.TabularInline):
    model = OTP
    extra = 0
    readonly_fields = ('code', 'created_at', 'expires_at')
    can_delete = False


# ========== MAIN ADMINS ==========

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model with enhanced features.
    """

    model = CustomUser
    form = CustomUserChangeForm

    # List display with useful information
    list_display = (
        'phone',
        'full_name',
        'email',
        'get_plans_display',
        'get_remaining_days_display',
        'has_card',
        'is_staff',
        'is_active',
        'date_joined'
    )

    # List filters for better navigation
    list_filter = (
        'is_staff',
        'is_active',
        'is_superuser',
        'plan__value',
        'date_joined',
        ('plan_expires_at', admin.DateFieldListFilter),
    )

    # Search capabilities
    search_fields = ('phone', 'full_name', 'email', 'username')
    ordering = ('-date_joined',)

    # Read-only fields
    readonly_fields = (
        'created_at',
        'updated_at',
        'last_login',
        'date_joined',
        'get_remaining_days_display',
        'get_active_plans_list'
    )

    # Optimized queryset
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'plan',
            'otps',
            Prefetch('user_card', queryset=UserCard.objects.select_related('template'))
        ).annotate(
            cards_count=Count('user_card')
        )

    # Custom display methods
    def get_plans_display(self, obj):
        """Display user's active plans."""
        plans = obj.get_active_plans()
        if plans:
            return ", ".join(plans)
        return "بدون پلن"
    get_plans_display.short_description = 'پلن‌های فعال'
    get_plans_display.admin_order_field = 'plan__value'

    def get_remaining_days_display(self, obj):
        """Display remaining days for plan expiration."""
        days = obj.get_remaining_days()
        if days is None:
            return "نامحدود"
        elif days <= 7:
            return f"⚠️ {days} روز"
        else:
            return f"{days} روز"
    get_remaining_days_display.short_description = 'انقضا پلن'

    def has_card(self, obj):
        """Check if user has created a business card."""
        return hasattr(obj, 'user_card') and obj.user_card is not None
    has_card.boolean = True
    has_card.short_description = 'کارت ویزیت'

    def get_active_plans_list(self, obj):
        """Display all active plans with details."""
        plans = obj.plan.all()
        if not plans:
            return "هیچ پلنی فعال نیست"

        plan_details = []
        for plan in plans:
            expiry = obj.get_remaining_days()
            expiry_text = f" (انقضا: {expiry} روز)" if expiry else " (نامحدود)"
            plan_details.append(f"{plan.value}{expiry_text}")

        return "\n".join(plan_details)
    get_active_plans_list.short_description = 'جزئیات پلن‌ها'

    # Fieldsets for better organization
    fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('phone', 'password')
        }),
        ('اطلاعات شخصی', {
            'fields': ('full_name', 'email', 'username')
        }),
        ('اشتراک و پلن', {
            'fields': ('plan', 'plan_expires_at', 'get_remaining_days_display', 'get_active_plans_list'),
            'classes': ('collapse',)
        }),
        ('دسترسی‌ها', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('تاریخچه', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Add form fieldsets
    add_fieldsets = (
        ('اطلاعات ورود', {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')
        }),
        ('اطلاعات شخصی', {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'username')
        }),
        ('اشتراک', {
            'classes': ('wide',),
            'fields': ('plan', 'plan_expires_at')
        }),
        ('دسترسی‌ها', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    # Actions
    actions = ['deactivate_users', 'activate_users']

    def deactivate_users(self, request, queryset):
        """Deactivate selected users."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} کاربر غیرفعال شدند.',
            level='SUCCESS'
        )
    deactivate_users.short_description = 'غیرفعال کردن کاربران انتخاب شده'

    def activate_users(self, request, queryset):
        """Activate selected users."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} کاربر فعال شدند.',
            level='SUCCESS'
        )
    activate_users.short_description = 'فعال کردن کاربران انتخاب شده'

    inlines = [OTPInline]


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """
    Admin interface for OTP model - read-only for security.
    """

    list_display = (
        'get_user_info',
        'code_masked',
        'created_at',
        'expires_at',
        'is_expired',
        'get_time_remaining'
    )
    search_fields = ('user__full_name', 'user__phone', 'code')
    list_filter = ('created_at', 'expires_at')
    readonly_fields = (
        'user',
        'code',
        'created_at',
        'expires_at',
        'is_expired',
        'get_time_remaining'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def get_user_info(self, obj):
        """Display user information."""
        return f"{obj.user.full_name or 'بدون نام'} ({obj.user.phone})"
    get_user_info.short_description = 'کاربر'
    get_user_info.admin_order_field = 'user__full_name'

    def code_masked(self, obj):
        """Display masked OTP code for security."""
        return f"{'*' * (len(obj.code) - 2)}{obj.code[-2:]}"
    code_masked.short_description = 'کد (مخفی)'

    def get_time_remaining(self, obj):
        """Display remaining time before expiration."""
        remaining = obj.get_time_remaining()
        if remaining is None:
            return "منقضی شده"
        minutes = int(remaining.total_seconds() / 60)
        return f"{minutes} دقیقه"
    get_time_remaining.short_description = 'زمان باقی‌مانده'

    def has_add_permission(self, request):
        """Disable adding OTPs manually."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing OTPs."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deleting expired OTPs."""
        if obj and obj.is_expired():
            return True
        return super().has_delete_permission(request, obj)


@admin.register(UserSubdomain)
class UserSubdomainAdmin(admin.ModelAdmin):
    list_display = ("subdomain", "user", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("subdomain", "user__username", "user__email", "user__phone")
    ordering = ("subdomain",)
