from django.contrib import admin

from .models import Product, UserShop


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = (
        "name",
        "price",
        "discount_percent",
        "final_price",
        "is_active",
    )
    readonly_fields = ("final_price",)


@admin.register(UserShop)
class UserShopAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "user__username", "user__full_name")
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "shop",
        "price",
        "discount_percent",
        "final_price",
        "is_active",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "shop__name", "shop__user__username")
