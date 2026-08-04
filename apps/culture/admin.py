from django.contrib import admin

# Register your models here.

from .models import (
    CultureArticle,
    CultureCategory,
    Proverb,
    ProverbCategory,
)


@admin.register(CultureCategory)
class CultureCategoryAdmin(admin.ModelAdmin):

    search_fields = (
        "name",
    )


@admin.register(CultureArticle)
class CultureArticleAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "published",
        "created_at",
    )

    list_filter = (
        "category",
        "published",
    )

    search_fields = (
        "title",
        "summary",
    )

    prepopulated_fields = {
        "slug": (
            "title",
        )
    }

@admin.register(ProverbCategory)
class ProverbCategoryAdmin(admin.ModelAdmin):

    search_fields = (
        "name",
    )


@admin.register(Proverb)
class ProverbAdmin(admin.ModelAdmin):

    list_display = (
        "short_proverb",
        "category",
        "dialect",
        "contributor",
        "status",
        "views",
        "likes",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "dialect",
    )

    search_fields = (
        "proverb",
        "english_translation",
        "meaning",
    )

    readonly_fields = (
        "views",
        "likes",
        "created_at",
        "updated_at",
    )

    actions = (
        "approve_selected",
        "reject_selected",
    )

    def short_proverb(self, obj):
        if obj.proverb:
            return obj.proverb[:40]
        return "Illustration Only"

    short_proverb.short_description = "Proverb"

    def approve_selected(self, request, queryset):
        queryset.update(status=Proverb.STATUS_APPROVED)

    approve_selected.short_description = (
        "Approve selected proverbs"
    )

    def reject_selected(self, request, queryset):
        queryset.update(status=Proverb.STATUS_REJECTED)

    reject_selected.short_description = (
        "Reject selected proverbs"
    )