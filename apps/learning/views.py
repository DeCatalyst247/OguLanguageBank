# Create your views here.
from django.shortcuts import get_object_or_404, render

from .models import Lesson


def lesson_list(request):

    lessons = Lesson.objects.filter(
        is_published=True,
    ).order_by("-created_at")

    context = {
        "lessons": lessons,
    }

    return render(
        request,
        "learning/lesson_list.html",
        context,
    )

def lesson_detail(request, slug):

    lesson = get_object_or_404(
        Lesson,
        slug=slug,
        is_published=True,
    )

    quizzes = lesson.quizzes.filter(
        is_active=True,
    )

    context = {

        "lesson": lesson,

        "quizzes": quizzes,

    }

    return render(

        request,

        "learning/lesson_detail.html",

        context,

    )