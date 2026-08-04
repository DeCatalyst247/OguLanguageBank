from django.contrib import admin

# Register your models here.
from .models import (
    Quiz,
    Question,
    Choice,
    QuizResult,
)


class ChoiceInline(admin.TabularInline):

    model = Choice

    extra = 4

    fields = (
        "option",
        "is_correct",
        "order",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "quiz",
        "marks",
        "order",
    )

    list_filter = (
        "quiz",
    )

    search_fields = (
        "question",
    )

    ordering = (
        "quiz",
        "order",
    )

    inlines = [
        ChoiceInline,
    ]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "lesson",
        "is_active",
        "passing_score",
        "time_limit",
        "created_at",
    )

    list_filter = (
        "lesson",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "lesson",
        "title",
    )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    list_display = (
        "option",
        "question",
        "is_correct",
        "order",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "option",
    )

    list_editable = (
        "is_correct",
    )


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "quiz",
        "score",
        "percentage",
        "passed",
        "completed_at",
    )

    list_filter = (
        "passed",
        "quiz",
    )

    search_fields = (
        "user__username",
        "quiz__title",
    )

    readonly_fields = (
        "completed_at",
    )

    ordering = (
        "-completed_at",
    )