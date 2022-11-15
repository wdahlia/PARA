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
        labels = {
            "content": "리뷰 내용",
            "grade": "평점",
            "review_image": "이미지",
        }


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
