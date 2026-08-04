from django import forms

from .models import WordRating


class WordRatingForm(forms.ModelForm):

    class Meta:

        model = WordRating

        fields = (
            "rating",
        )

        widgets = {

            "rating": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

        }