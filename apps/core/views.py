from django.shortcuts import render
from datetime import date
from django.db.models import Q, connection



from apps.culture.models import (
    CultureArticle,
    Proverb,
)
from apps.dictionary.models import(
    Word,
    Category,
    Dialect,
    WordOfTheDay,
)
from .forms import ContactForm
from apps.learning.models import Lesson
from apps.quiz.models import Quiz
from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.




def home(request):
    print("DATABASE ENGINE:", connection.vendor)
    print("DATABASE NAME:", connection.settings_dict.get("NAME"))

    word_of_the_day = WordOfTheDay.objects.select_related(
        "word",
    ).first()

   # latest_words = Word.objects.filter(
    #    status="approved",
    #)[:8]

    latest_words = Word.objects.filter(
        status="published"
    ).order_by("-created_at")[:6]

    featured_lesson = Lesson.objects.first()

    featured_quiz = Quiz.objects.filter(
        is_active=True,
    ).first()

    featured_proverb = Proverb.objects.filter(
        status=Proverb.STATUS_APPROVED,
    ).first()

    latest_articles = CultureArticle.objects.filter(
        published=True,
    )[:3]

    context = {

        "word_of_the_day": word_of_the_day,

        "latest_words": latest_words,

        "featured_lesson": featured_lesson,

        "featured_quiz": featured_quiz,

        "featured_proverb": featured_proverb,

        "latest_articles": latest_articles,

        "word_count": Word.objects.count(),

        "lesson_count": Lesson.objects.count(),

        "quiz_count": Quiz.objects.count(),

        "proverb_count": Proverb.objects.count(),

    }
    



    return render(
        request,
        "core/home.html",
        context,
    )






def about(request):

    return render(

        request,

        "core/about.html",

    )


def contact(request):

    if request.method == "POST":

        form = ContactForm(

            request.POST,

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Thank you for contacting us. We will get back to you soon.",

            )

            return redirect(

                "core:contact",

            )

    else:

        form = ContactForm()

    return render(

        request,

        "core/contact.html",

        {

            "form": form,

        },

    )



def global_search(request):

    query = request.GET.get(
        "q",
        "",
    )

    words = []

    lessons = []

    articles = []

    proverbs = []

    festivals = []

    historical_figures = []

    if query:

        words = Word.objects.filter(

            Q(ogu_word__icontains=query)

            | Q(translations__translation__icontains=query)

            | Q(meanings__meaning__icontains=query)

        ).distinct()

        lessons = Lesson.objects.filter(

            is_published=True,

            title__icontains=query,

        )

        articles = CultureArticle.objects.filter(

            published=True,

            title__icontains=query,

        )

        proverbs = Proverb.objects.filter(

            proverb__icontains=query,

        )

        festivals =[] 
        '''Festival.objects.filter(

            name__icontains=query,

        )'''

        historical_figures =[]
        ''' HistoricalFigure.objects.filter(

            name__icontains=query,

        )
'''
    context = {

        "query": query,

        "words": words,

        "lessons": lessons,

        "articles": articles,

        "proverbs": proverbs,

        "festivals": festivals,

        "historical_figures": historical_figures,

    }

    return render(

        request,

        "core/search.html",

        context,

    )



def custom_404(request, exception):

    return render(

        request,

        "errors/404.html",

        status=404,

    )


def custom_500(request):

    return render(

        request,

        "errors/500.html",

        status=500,

    )