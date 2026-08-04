from django.db import models

# Create your models here.
from django.conf import settings

from apps.dictionary.models import Word


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "user",
            "word",
        )

        ordering = (
            "-created_at",
        )

    def __str__(self):
        return f"{self.user.username} ❤️ {self.word.ogu_word}"



class WordRating(models.Model):

    RATINGS = (
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATINGS,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "user",
            "word",
        )

    def __str__(self):
        return f"{self.word} ({self.rating})"



class RecentlyViewed(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recently_viewed",
    )

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="recent_views",
    )

    viewed_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = (
            "-viewed_at",
        )

        unique_together = (
            "user",
            "word",
        )

    def __str__(self):
        return f"{self.user.username} viewed {self.word.ogu_word}"