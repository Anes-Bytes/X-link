from django.contrib import admin

from .models import CardTemplate, TemplateSelection


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "template_id", "category", "is_active")
    search_fields = ("name", "template_id", "category")
    list_filter = ("category", "is_active")
    readonly_fields = ("created_at", "updated_at")


@admin.register(TemplateSelection)
class TemplateSelectionAdmin(admin.ModelAdmin):
    list_display = ("template", "user", "session_id", "created_at")
    search_fields = ("template__name", "template__template_id", "session_id")
    list_filter = ("template__category",)
    readonly_fields = ("created_at", "updated_at")
