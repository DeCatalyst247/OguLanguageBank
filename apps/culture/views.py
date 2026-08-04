from django.shortcuts import render

# Create your views here.
from django.shortcuts import (
    get_object_or_404,
    render,
)
from apps.dictionary.models import Dialect
from .models import (
    CultureArticle,
    CultureCategory,
    Proverb,
    ProverbCategory,
)


def culture_home(request):

    latest_articles = CultureArticle.objects.filter(
        published=True,
    ).order_by(
        "-created_at",
    )[:6]

    categories = CultureCategory.objects.all()

    return render(
        request,
        "culture/home.html",
        {
            "articles": latest_articles,
            "categories": categories,
        },
    )


def article_list(request):

    articles = CultureArticle.objects.filter(
        published=True,
    )

    categories = CultureCategory.objects.all()

    search = request.GET.get("search")

    category = request.GET.get("category")

    if search:

        articles = articles.filter(
            title__icontains=search,
        )

    if category:

        articles = articles.filter(
            category_id=category,
        )

    return render(
        request,
        "culture/article_list.html",
        {
            "articles": articles,
            "categories": categories,
        },
    )


def article_detail(request, slug):

    article = get_object_or_404(
        CultureArticle,
        slug=slug,
        published=True,
    )

    related_articles = CultureArticle.objects.filter(
        category=article.category,
        published=True,
    ).exclude(
        id=article.id,
    )[:4]

    return render(
        request,
        "culture/article_detail.html",
        {
            "article": article,
            "related_articles": related_articles,
        },
    )



def proverb_list(request):

    proverbs = Proverb.objects.filter(
        status=Proverb.STATUS_APPROVED,
    )

    categories = ProverbCategory.objects.all()

    search = request.GET.get("search")

    category = request.GET.get("category")

    dialect = request.GET.get("dialect")

    if search:

        proverbs = proverbs.filter(
            proverb__icontains=search,
        )

    if category:

        proverbs = proverbs.filter(
            category_id=category,
        )

    if dialect:

        proverbs = proverbs.filter(
            dialect_id=dialect,
        )

    proverbs = proverbs.order_by(
        "-created_at",
    )

    return render(

        request,

        "culture/proverb_list.html",

        {
            "proverbs": proverbs,
            "categories": categories,
            "dialects": Dialect.objects.all(),
        },

    )

def proverb_detail(request, pk):

    proverb = get_object_or_404(
        Proverb,
        pk=pk,
        status=Proverb.STATUS_APPROVED,
    )

    proverb.views += 1
    proverb.save(update_fields=["views"])

    return render(
        request,
        "culture/proverb_detail.html",
        {
            "proverb": proverb,
        },
    )