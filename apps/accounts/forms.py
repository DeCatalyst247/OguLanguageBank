from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "profile_picture",
            "bio",
            "preferred_dialect",
            "location",
            "website",
            "github",
        ]