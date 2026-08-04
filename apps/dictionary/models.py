from django.db import models
from django.db.models import Avg

# Create your models here.
from apps.core.models import TimeStampedModel
from django.conf import settings
from django.utils.text import slugify
from apps.core.choices import Difficulty,Status
from apps.core.models import TimeStampedModel


class Dialect(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    region = models.CharField(max_length=150)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class PartOfSpeech(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Parts of Speech"

    def __str__(self):
        return self.name


class Word(TimeStampedModel):
    ogu_word = models.CharField(max_length=150, unique=True)

    slug = models.SlugField(max_length=180, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="words",
    )

    dialect = models.ForeignKey(
        Dialect,
        on_delete=models.PROTECT,
        related_name="words",
    )

    part_of_speech = models.ForeignKey(
        PartOfSpeech,
        on_delete=models.PROTECT,
        related_name="words",
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )

    etymology = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    @property
    def average_rating(self):

        average = self.ratings.aggregate(
            Avg("rating")
        )["rating__avg"]

        if average is None:
            return 0

        return round(
            average,
            1,
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_words",
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_words",
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    views = models.PositiveIntegerField(default=0)

    search_count = models.PositiveIntegerField(default=0)

    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ogu_word"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ogu_word)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ogu_word



class EnglishTranslation(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    translation = models.CharField(max_length=200)

    notes = models.TextField(blank=True)

    priority = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return self.translation

class Meaning(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="meanings",
    )

    meaning = models.TextField()

    context = models.CharField(
        max_length=150,
        blank=True,
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.meaning[:50]


class ExampleSentence(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="examples",
    )

    ogu_sentence = models.TextField()

    english_sentence = models.TextField()

    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.ogu_sentence[:50]


class Pronunciation(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="pronunciations",
    )

    dialect = models.ForeignKey(
        Dialect,
        on_delete=models.PROTECT,
        related_name="pronunciations",
    )

    audio = models.FileField(
        upload_to="pronunciations/",
        blank=True,
        null=True,
    )

    pronunciation_text = models.CharField(
        max_length=200,
        blank=True,
    )

    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    votes = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.word} ({self.dialect})"


class Synonym(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="synonyms",
    )

    synonym = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="synonym_of",
    )

    def __str__(self):
        return f"{self.word} → {self.synonym}"

class Antonym(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="antonyms",
    )

    antonym = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="antonym_of",
    )

    def __str__(self):
        return f"{self.word} ↔️ {self.antonym}"

class RelatedWord(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="related_words",
    )

    related_word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="related_to",
    )

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return f"{self.word} → {self.related_word}"

class AlternativeSpelling(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="alternative_spellings",
    )

    spelling = models.CharField(max_length=150)

    def __str__(self):
        return self.spelling

class WordImage(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="word_images/",
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.word.ogu_word

class WordVideo(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="videos",
    )

    video = models.FileField(
        upload_to="word_videos/",
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class WordOfTheDay(TimeStampedModel):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="daily_features",
    )

    date = models.DateField(unique=True)

    note = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Word of the Day"
        verbose_name_plural = "Words of the Day"

    def __str__(self):
        return f"{self.date} - {self.word.ogu_word}"


class WordContribution(models.Model):

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="word_contributions",
    )

    ogu_word = models.CharField(max_length=255)

    english_translation = models.CharField(max_length=255)

    meaning = models.TextField()

    example_sentence = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    admin_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_contributions",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    approved_word = models.OneToOneField(
        "Word",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contribution",


    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    dialect = models.ForeignKey(
        Dialect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    part_of_speech = models.ForeignKey(
        PartOfSpeech,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )


    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.ogu_word} ({self.status})"


class Comment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    comment = models.TextField()

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    is_approved = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False,)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username


class CommentLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        unique_together = (
            "user",
            "comment",
        )

    def __str__(self):
        return f"{self.user} likes Comment {self.comment.id}"