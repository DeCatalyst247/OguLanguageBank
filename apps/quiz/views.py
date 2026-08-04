# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import (
    Choice,
    Quiz,
    QuizResult,
)

def quiz_list(request):

    quizzes = Quiz.objects.filter(
        is_active=True,
    ).select_related(
        "lesson",
    )

    context = {
        "quizzes": quizzes,
    }

    return render(
        request,
        "quiz/quiz_list.html",
        context,
    )


@login_required
def quiz_detail(request, pk):

    quiz = get_object_or_404(
        Quiz,
        pk=pk,
        is_active=True,
    )

    if request.method == "POST":

        score = 0

        total = quiz.questions.count()

        for question in quiz.questions.all():

            selected_choice = request.POST.get(
                f"question_{question.id}"
            )

            if selected_choice:

                choice = Choice.objects.get(
                    pk=selected_choice
                )

                if choice.is_correct:

                    score += question.marks

        maximum_marks = sum(
            question.marks
            for question in quiz.questions.all()
        )

        percentage = 0

        if maximum_marks > 0:

            percentage = (
                score / maximum_marks
            ) * 100

        passed = (
            percentage >= quiz.passing_score
        )

        result = QuizResult.objects.create(

            user=request.user,

            quiz=quiz,

            score=score,

            total_questions=total,

            percentage=percentage,

            passed=passed,

        )

        return redirect(

            "quiz:quiz_result",

            pk=result.pk,

        )

    context = {

        "quiz": quiz,

    }

    return render(

        request,

        "quiz/quiz_detail.html",

        context,

    )

@login_required
def quiz_result(request, pk):

    result = get_object_or_404(

        QuizResult,

        pk=pk,

        user=request.user,

    )

    context = {

        "result": result,

    }

    return render(

        request,

        "quiz/quiz_result.html",

        context,

    )


@login_required
def quiz_history(request):

    results = QuizResult.objects.filter(

        user=request.user,

    ).select_related(

        "quiz",

    ).order_by(

        "-completed_at",

    )

    context = {

        "results": results,

    }

    return render(

        request,

        "quiz/quiz_history.html",

        context,

    )