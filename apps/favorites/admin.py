from django.contrib import admin

# Register your models here.
from .models import Favorite, WordRating,RecentlyViewed


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "word",
        "created_at",
    )

    search_fields = (
        "user__username",
        "word__ogu_word",
    )


@admin.register(WordRating)
class WordRatingAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "word",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
    )

    search_fields = (
        "user__username",
        "word__ogu_word",
    )

@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "word",
        "viewed_at",
    )

    search_fields = (
        "user__username",
        "word__ogu_word",
    )

    ordering = (
        "-viewed_at",
    )