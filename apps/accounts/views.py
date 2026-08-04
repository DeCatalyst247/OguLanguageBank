from django.shortcuts import render,redirect

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import ProfileForm
from .models import Profile
from apps.dictionary.models import WordContribution
from apps.favorites.models import (
    Favorite,
    WordRating,
)
def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Registration successful."
            )

            return redirect("core:home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def user_login(request):

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            login(request, form.get_user())

            return redirect("core:home")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )

@login_required
def profile(request):

    profile,created =Profile.objects.get_or_create(user=request.user)

    context = {
        "profile": profile,
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )


@login_required
def edit_profile(request):

    profile,created =Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("accounts:profile")

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )
def user_logout(request):

    logout(request)

    return redirect("core:home")


@login_required
def dashboard(request):

    favorite_count = Favorite.objects.filter(
        user=request.user,
    ).count()

    contribution_count = WordContribution.objects.filter(
        contributor=request.user,
    ).count()

    rating_count = WordRating.objects.filter(
        user=request.user,
    ).count()

    context = {

        "favorite_count": favorite_count,

        "contribution_count": contribution_count,

        "rating_count": rating_count,

    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )