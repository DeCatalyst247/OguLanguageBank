from django.shortcuts import render

# Create your views here.
from .models import RecentlyViewed
from django.contrib.auth.decorators import login_required

@login_required
def recently_viewed(request):

    words = RecentlyViewed.objects.filter(
        user=request.user,
    ).select_related(
        "word",
    )

    return render(
        request,
        "favorites/recently_viewed.html",
        {
            "words": words,
        },
    )