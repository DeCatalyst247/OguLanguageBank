from django.contrib import admin

# Register your models here.


from .models import (
    GrammarTopic,
    Lesson,
    LessonCategory,
)


@admin.register(LessonCategory)
class LessonCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


class GrammarTopicInline(admin.TabularInline):

    model = GrammarTopic

    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "level",
        "is_published",
        "created_at",
    )

    list_filter = (
        "category",
        "level",
        "is_published",
    )

    search_fields = (
        "title",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [
        GrammarTopicInline,
    ]