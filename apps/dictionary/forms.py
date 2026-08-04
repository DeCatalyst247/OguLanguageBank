from django import forms

from .models import WordContribution,Word,Comment


class WordContributionForm(forms.ModelForm):

    class Meta:
        model = WordContribution

        fields = [
            "ogu_word",
            "english_translation",
            "meaning",
            "example_sentence",
            "category",
            "dialect",
            "part_of_speech",
            "difficulty",
        ]

class WordForm(forms.ModelForm):
    class Meta:
        model =Word
        exclude = (
            "slug",
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["comment"]

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Write your comment...",
                }
            )
        }