from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Customers, Templates, SiteContext, Plan, Discount, Feature, UserCard, Skill, Banners


# ========== Inline ADMINS ==========
class FeaturesInline(admin.TabularInline):
    model = Feature
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


# ========== MAIN ADMINS ==========

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('company_name',)
    search_fields = ('company_name',)


@admin.register(Plan)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [FeaturesInline]


@admin.register(SiteContext)
class SiteContextAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    search_fields = ('site_name',)


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'user', 'color', 'is_published', 'created_at')
    list_filter = ('color', 'is_published', 'created_at')
    search_fields = ('name', 'username', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SkillInline]
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'username', "profile_picture",'template')
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


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_card', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user_card__name')
    readonly_fields = ('created_at',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # نمایش ستون‌ها در لیست کاربران
    list_display = ('phone', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # فیلد مرتب‌سازی
    ordering = ('phone',)

    # فیلدهایی که در صفحه جزئیات نمایش داده می‌شوند
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # فیلدهایی که هنگام ایجاد کاربر نمایش داده می‌شوند
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('phone', 'full_name')



admin.site.register(Discount)
admin.site.register(Banners)