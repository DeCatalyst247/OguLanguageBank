from django.conf import settings
from django.db import models

from apps.learning.models import Lesson


class Quiz(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="quizzes",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    time_limit = models.PositiveIntegerField(
        default=10,
        help_text="Time limit in minutes",
    )

    passing_score = models.PositiveIntegerField(
        default=50,
        help_text="Percentage required to pass",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title



class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question = models.TextField()

    explanation = models.TextField(
        blank=True,
    )

    marks = models.PositiveIntegerField(
        default=1,
    )

    order = models.PositiveIntegerField(
        default=1,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.question



class Choice(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )

    option = models.CharField(
        max_length=300,
    )

    is_correct = models.BooleanField(
        default=False,
    )

    order = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return self.option



class QuizResult(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="results",
    )

    score = models.PositiveIntegerField(
        default=0,
    )

    total_questions = models.PositiveIntegerField(
        default=0,
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    passed = models.BooleanField(
        default=False,
    )

    completed_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.quiz.title}"
        )