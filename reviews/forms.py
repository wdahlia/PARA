from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "content",
            "grade",
            "review_image",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"class": "from-control", "rows": 1})
        }
        labels = {
            "content": "댓글",
        }
