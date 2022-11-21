from django import forms
from .models import Review, Comment
from django.forms import TextInput, PasswordInput, EmailInput, FileInput, Select
from taggit.managers import TaggableManager

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "content",
            "grade",
            "review_image",
            "tags",
        ]
        labels = {
            "content": "리뷰 내용",
            "grade": "평점",
            "review_image": "이미지",
            "tags": "해시태그",
        }

        widgets = {
            "content": TextInput(
                attrs={
                    "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                    "style": "background: transparent;",
                    "placeholder": "리뷰를 입력해주세요",
                }
            ),
            "grade": Select(
                attrs={
                    "style": "background: transparent;",
                }
            ),
            "review_image": FileInput(
                attrs={
                    "style": "background: transparent;",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 2,
                    "style": "background: transparent;",
                    "class": "border border-2 border-dark bg-white rounded-1 text-dark p-3 font-space shadow-sm scroll-none",
                }
            ),
        }

        labels = {
            "content": "",
        }
