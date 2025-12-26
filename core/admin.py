from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Prefetch, Count, Q

from cards.models import UserCard
from .models import CustomUser, UserMessages, OTP


# ========== Inline ADMINS ==========

class UserMessagesInline(admin.TabularInline):
    model = UserMessages
    extra = 0


class OTPInline(admin.TabularInline):
    model = OTP
    extra = 0
    readonly_fields = ('code', 'created_at', 'expires_at')
    can_delete = False


# ========== MAIN ADMINS ==========

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