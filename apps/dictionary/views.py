from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from apps.favorites.models import Favorite,WordRating,RecentlyViewed
from apps.favorites.forms import WordRatingForm
from .models import Word,Category,Dialect,PartOfSpeech,WordContribution,Comment
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import WordContributionForm,WordForm,CommentForm
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required



#def word_list(request):

  #  words = Word.objects.filter(
 #       status="published",
#    ).select_related(

def word_list(request):

    print("DATABASE ENGINE:", connection.vendor)
    print("DATABASE HOST:", connection.settings_dict.get("HOST"))
    print("DATABASE NAME:", connection.settings_dict.get("NAME"))
    print("TOTAL WORDS:", Word.objects.count())
    print("WORD STATUSES:", list(
        Word.objects.values_list("status", flat=True)
    ))

    words = Word.objects.filter(
        status="published",
    ).select_related(
        "category",
        "dialect",
        "part_of_speech",
    )



    search = request.GET.get("search")
    category = request.GET.get("category")
    dialect = request.GET.get("dialect")
    part = request.GET.get("part")
    difficulty = request.GET.get("difficulty")

    # Search
    if search:
        words = words.filter(
            Q(ogu_word__icontains=search) |
            Q(translations__translation__icontains=search)
        ).distinct()

    # Category filter
    if category:
        words = words.filter(
            category_id=category
        )

    # Dialect filter
    if dialect:
        words = words.filter(
            dialect_id=dialect
        )

    # Part of speech filter
    if part:
        words = words.filter(
            part_of_speech_id=part
        )

    # Difficulty filter
    if difficulty:
        words = words.filter(
            difficulty=difficulty
        )

    # Pagination (AFTER filtering)
    paginator = Paginator(words, 12)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "words": page_obj,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "dialects": Dialect.objects.all(),
        "parts": PartOfSpeech.objects.all(),
        "search": search,
        "selected_category": category,
        "selected_dialect": dialect,
        "selected_part": part,
        "selected_difficulty": difficulty,
    }

    return render(
        request,
        "dictionary/word_list.html",
        context,
    )


@staff_member_required
def review_contribution(request, pk):

    contribution = get_object_or_404(
        WordContribution,
        pk=pk,
    )

    if request.method == "POST":

        form = WordForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            word = form.save(commit=False)

            word.ogu_word = contribution.ogu_word
            word.slug = slugify(contribution.ogu_word)

            word.save()

            contribution.status = (
                WordContribution.STATUS_APPROVED
            )

            contribution.approved_word = word

            contribution.save()

            return redirect("/admin/dictionary/word/")

    else:

        form = WordForm(
            initial={
                "ogu_word": contribution.ogu_word,
            }
        )

    return render(
        request,
        "dictionary/review_contribution.html",
        {
            "form": form,
            "contribution": contribution,
        },
    )

def word_detail(request, slug):

    word = get_object_or_404(
        Word.objects.select_related(
            "category",
            "dialect",
            "part_of_speech",
        ).prefetch_related(
            "translations",
            "meanings",
            "examples",
            "pronunciations",
            "alternative_spellings",
            "images",
            "videos",
        ),
        slug=slug,
        status="published",
    )
    comments = Comment.objects.filter(
        word=word,
        parent__isnull=True,
        is_approved=True,
    ).select_related("user").prefetch_related(
        "replies",
    )
    word.views += 1
    word.save(update_fields=["views"])
    is_favorite = False
    
    if request.user.is_authenticated:

        is_favorite = Favorite.objects.filter(
            user=request.user,
            word=word,
        ).exists()

        RecentlyViewed.objects.update_or_create(
            user=request.user,
            word=word,
        )
    context = {
    "word": word,
    "translations": word.translations.all(),
    "meanings": word.meanings.all(),
    "examples": word.examples.all(),
    "pronunciations": word.pronunciations.all(),
    "alternative_spellings": word.alternative_spellings.all(),
    "synonyms": word.synonyms.all(),
    "antonyms": word.antonyms.all(),
    "related_words": word.related_words.all(),
    "images": word.images.all(),
    "videos": word.videos.all(),
    "comments":comments,
    "comment_form":CommentForm(),
    "is_favorite":is_favorite,
}
    return render(
        request,
        "dictionary/word_detail.html",
        context,
    )


@login_required
def contribute_word(request):

    if request.method == "POST":

        form = WordContributionForm(request.POST)

        if form.is_valid():

            contribution = form.save(commit=False)

            contribution.contributor = request.user

            contribution.save()

            return redirect("dictionary:my_contributions")

    else:

        form = WordContributionForm()

    return render(
        request,
        "dictionary/contribute_word.html",
        {
            "form": form,
        },
    )


@login_required
def my_contributions(request):

    contributions = WordContribution.objects.filter(
        contributor=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dictionary/my_contributions.html",
        {
            "contributions": contributions,
        },
    )



def moderation_dashboard(request):

    stats = WordContribution.objects.aggregate(
        total=Count("id"),
    )

    pending = WordContribution.objects.filter(
        status=WordContribution.STATUS_PENDING
    ).count()

    approved = WordContribution.objects.filter(
        status=WordContribution.STATUS_APPROVED
    ).count()

    rejected = WordContribution.objects.filter(
        status=WordContribution.STATUS_REJECTED
    ).count()

    return render(
        request,
        "dictionary/moderation_dashboard.html",
        {
            "stats": stats,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        },
    )

@login_required
def add_to_favorites(request, slug):

    word = get_object_or_404(
        Word,
        slug=slug,
    )

    Favorite.objects.get_or_create(
        user=request.user,
        word=word,
    )

    return redirect(
        "dictionary:word_detail",
        slug=slug,
    )

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("word")

    return render(request,"dictionary/my_favorites.html",{"favorites": favorites,},
    )
@login_required
def remove_favorites(request, slug):

    word = get_object_or_404(
        Word,
        slug=slug,
    )

    Favorite.objects.filter(
        user=request.user,
        word=word,
        ).delete()
    

    return redirect(
        "dictionary:my_favorites",
    )

@login_required
def rate_word(request, slug):

    word = get_object_or_404(
        Word,
        slug=slug,
    )

    try:
        rating = WordRating.objects.get(
            user=request.user,
            word=word,
        )
    except WordRating.DoesNotExist:
        rating = None

    if request.method == "POST":

        form = WordRatingForm(
            request.POST,
            instance=rating,
        )

        if form.is_valid():

            rating = form.save(commit=False)
            rating.user = request.user
            rating.word = word
            rating.save()

            return redirect(
                "dictionary:word_detail",
                slug=slug,
            )

    else:

        form = WordRatingForm(
            instance=rating,
        )

    return render(
        request,
        "dictionary/rate_word.html",
        {
            "word": word,
            "form": form,
        },
    )


@login_required
def add_comment(request, slug):
    word = get_object_or_404(
        Word,
        slug=slug,
    )

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.word = word

            comment.user = request.user

            comment.save()

    return redirect(
        "dictionary:word_detail",
        slug=word.slug,
    )

@login_required
def reply_comment(request, comment_id):

    parent_comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            reply = form.save(commit=False)

            reply.word = parent_comment.word

            reply.user = request.user

            reply.parent = parent_comment

            reply.save()

    return redirect(
        "dictionary:word_detail",
        slug=parent_comment.word.slug,
    )



@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    if comment.user != request.user:
        return HttpResponseForbidden(
            "You cannot edit this comment."
        )

    if request.method == "POST":

        form = CommentForm(
            request.POST,
            instance=comment,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Comment updated successfully.",
            )

            return redirect(
                "dictionary:word_detail",
                slug=comment.word.slug,
            )

    else:

        form = CommentForm(
            instance=comment,
        )

    return render(
        request,
        "dictionary/edit_comment.html",
        {
            "form": form,
            "comment": comment,
        },
    )

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    if comment.user != request.user:

        return HttpResponseForbidden(
            "You cannot delete this comment."
        )

    word_slug = comment.word.slug

    comment.delete()

    messages.success(
        request,
        "Comment deleted successfully.",
    )

    return redirect(
        "dictionary:word_detail",
        slug=word_slug,
    )


@login_required
def like_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment,
    )

    return redirect(
        "dictionary:word_detail",
        slug=comment.word.slug,
    )

@login_required
def report_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    comment.is_reported = True

    comment.save()

    messages.success(
        request,
        "Comment reported.",
    )

    return redirect(
        "dictionary:word_detail",
        slug=comment.word.slug,
    )