from django.contrib import admin
from django.utils.text import slugify
from django.utils import timezone
from apps.core.choices import Status
from apps.favorites.models import Favorite,WordRating
from .models import (
    AlternativeSpelling,
    Antonym,
    Category,
    Dialect,
    EnglishTranslation,
    ExampleSentence,
    Meaning,
    PartOfSpeech,
    Pronunciation,
    RelatedWord,
    Synonym,
    Word,
    WordContribution,
    WordImage,
    WordOfTheDay,
    WordVideo,
)


# ==========================
# Inline Models
# ==========================

class EnglishTranslationInline(admin.TabularInline):
    model = EnglishTranslation
    extra = 1


class MeaningInline(admin.TabularInline):
    model = Meaning
    extra = 1


class ExampleSentenceInline(admin.TabularInline):
    model = ExampleSentence
    extra = 1


class PronunciationInline(admin.TabularInline):
    model = Pronunciation
    extra = 1


class AlternativeSpellingInline(admin.TabularInline):
    model = AlternativeSpelling
    extra = 1


class WordImageInline(admin.TabularInline):
    model = WordImage
    extra = 1


class WordVideoInline(admin.TabularInline):
    model = WordVideo
    extra = 1


# ==========================
# Word Admin
# ==========================

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):

    list_display = (
        "ogu_word",
        "category",
        "dialect",
        "part_of_speech",
        "difficulty",
        "status",
        "views",
        "likes",
        "search_count",
        "created_at",
    )

    list_filter = (
        "category",
        "dialect",
        "part_of_speech",
        "difficulty",
        "status",
        "created_at",
    )

    search_fields = (
        "ogu_word",
        "slug",
        "etymology",
    )

    actions = (
        "approve_selected",
        "reject_selected",
    )
    def approve_selected(self, request, queryset):
        queryset.update(
            status=Word.Status.PUBLISHED,
            approved_by=request.user,
            approved_at=timezone.now(),
        )

    approve_selected.short_description = "Approve selected words"


    def reject_selected(self, request, queryset):
        queryset.update(
            status=Word.Status.DRAFT,
        )

    reject_selected.short_description = "Reject selected words"
    ordering = (
        "ogu_word",
    )

    list_per_page = 25

    prepopulated_fields = {
        "slug": ("ogu_word",)
    }

    readonly_fields = (
        "views",
        "likes",
        "search_count",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "ogu_word",
                    "slug",
                    "category",
                    "dialect",
                    "part_of_speech",
                )
            },
        ),

        (
            "Dictionary Details",
            {
                "fields": (
                    "difficulty",
                    "status",
                    "etymology",
                )
            },
        ),

        (
            "Statistics",
            {
                "fields": (
                    "views",
                    "likes",
                    "search_count",
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )

    inlines = [
        EnglishTranslationInline,
        MeaningInline,
        ExampleSentenceInline,
        PronunciationInline,
        AlternativeSpellingInline,
        WordImageInline,
        WordVideoInline,
    ]


# ==========================
# Word Contribution Admin
# ==========================


@admin.register(WordContribution)
class WordContributionAdmin(admin.ModelAdmin):

    list_display = (
        "ogu_word",
        "contributor",
        "status",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
        "reviewed_at",
    )

    search_fields = (
        "ogu_word",
        "english_translation",
        "meaning",
        "contributor__username",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "reviewed_at",
        "approved_word",
    )

    fieldsets = (
        (
            "Contribution Information",
            {
                "fields": (
                    "contributor",
                    "ogu_word",
                    "english_translation",
                    "meaning",
                    "example_sentence",
                )
            },
        ),
        (
            "Dictionary Information",
            {
                "fields": (
                    "category",
                    "dialect",
                    "part_of_speech",
                    "difficulty",
                )
            },
        ),
        (
            "Moderation",
            {
                "fields": (
                    "status",
                    "admin_note",
                    "reviewed_by",
                    "reviewed_at",
                    "approved_word",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = (
        "approve_selected",
        "reject_selected",
    )

    def save_model(self, request, obj, form, change):

        if obj.status != WordContribution.STATUS_PENDING:

            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()

        super().save_model(
            request,
            obj,
            form,
            change,
        )

    def approve_selected(self, request, queryset):

        for contribution in queryset.filter(
            status=WordContribution.STATUS_PENDING
        ):

            # Already approved before
            if contribution.approved_word:
                continue

            # Create the dictionary word
            word = Word.objects.create(
                ogu_word=contribution.ogu_word,
                slug=slugify(contribution.ogu_word),
                category=contribution.category,
                dialect=contribution.dialect,
                part_of_speech=contribution.part_of_speech,
                difficulty=contribution.difficulty,
                status= Status.PUBLISHED,
                created_by=contribution.contributor,
                approved_by=request.user,
                approved_at=timezone.now(),
            )

            # English Translation
            EnglishTranslation.objects.create(
                word=word,
                translation=contribution.english_translation,
            )

            # Meaning
            Meaning.objects.create(
                word=word,
                meaning=contribution.meaning,
            )

            # Example Sentence
            if contribution.example_sentence:
                ExampleSentence.objects.create(
                    word=word,
                    ogu_sentence=contribution.example_sentence,
                    english_sentence="",
                    contributor=contribution.contributor,
                )

            # Link contribution to created word
            contribution.status = WordContribution.STATUS_APPROVED
            contribution.reviewed_by = request.user
            contribution.reviewed_at = timezone.now()
            contribution.approved_word = word

            contribution.save()


    approve_selected.short_description = (
        "Approve selected contributions"
    )

    def reject_selected(self, request, queryset):

        queryset.update(
            status=WordContribution.STATUS_REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    reject_selected.short_description = (
        "Reject selected contributions"
    )




# ==========================
# Category
# ==========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================
# Dialect
# ==========================

@admin.register(Dialect)
class DialectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================
# Part Of Speech
# ==========================

@admin.register(PartOfSpeech)
class PartOfSpeechAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================
# Synonym
# ==========================

@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin):

    list_display = (
        "word",
        "synonym",
    )

    search_fields = (
        "word__ogu_word",
        "synonym",
    )


# ==========================
# Antonym
# ==========================

@admin.register(Antonym)
class AntonymAdmin(admin.ModelAdmin):

    list_display = (
        "word",
        "antonym",
    )

    search_fields = (
        "word__ogu_word",
        "antonym",
    )


# ==========================
# Related Word
# ==========================

@admin.register(RelatedWord)
class RelatedWordAdmin(admin.ModelAdmin):

    list_display = (
        "word",
        "related_word",
    )

    search_fields = (
        "word__ogu_word",
        "related_word",
    )


# ==========================
# Word Of The Day
# ==========================

@admin.register(WordOfTheDay)
class WordOfTheDayAdmin(admin.ModelAdmin):

    list_display = (
        "word",
        "date",
    )

    ordering = (
        "-date",
    )
