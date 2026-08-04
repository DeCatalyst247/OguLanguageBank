from django.db import models

# Create your models here.
from django.conf import settings

from apps.dictionary.models import Dialect


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    full_name = models.CharField(
        max_length=150,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    bio = models.TextField(blank=True)

    preferred_dialect = models.ForeignKey(
        Dialect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    website = models.URLField(blank=True)

    github = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username