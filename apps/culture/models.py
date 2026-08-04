from django.db import models

# Create your models here.
from django.utils.text import slugify


class CultureCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class CultureArticle(models.Model):

    category = models.ForeignKey(
        CultureCategory,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    summary = models.TextField()

    content = models.TextField()

    image = models.ImageField(
        upload_to="culture/",
        blank=True,
        null=True,
    )

    published = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class ProverbCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class Proverb(models.Model):

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    )

    category = models.ForeignKey(
        ProverbCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    dialect = models.ForeignKey(
        "dictionary.Dialect",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    contributor = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="proverbs",
    )

    proverb = models.TextField(
        blank=True,
        help_text="Leave empty if only uploading an illustration.",
    )

    english_translation = models.TextField(
        blank=True,
    )

    meaning = models.TextField()

    usage = models.TextField(
        blank=True,
    )

    illustration = models.ImageField(
        upload_to="proverbs/",
        blank=True,
        null=True,
    )

    audio = models.FileField(
        upload_to="proverbs/audio/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    views = models.PositiveIntegerField(
        default=0,
    )

    likes = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        if self.proverb:
            return self.proverb[:50]
        return f"Illustrated Proverb #{self.pk}"