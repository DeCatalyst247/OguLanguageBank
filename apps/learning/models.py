from django.db import models

# Create your models here.
class LessonCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

    LEVELS = (
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    category = models.ForeignKey(
        LessonCategory,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        unique=True,
    )

    content = models.TextField()

    level = models.CharField(
        max_length=20,
        choices=LEVELS,
        default=BEGINNER,
    )

    is_published = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title


class GrammarTopic(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="grammar_topics",
    )

    title = models.CharField(
        max_length=200,
    )

    explanation = models.TextField()

    example = models.TextField()

    def __str__(self):
        return self.title