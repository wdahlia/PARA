from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    ReadOnlyPasswordHashField
)
from django import forms
from django.forms import TextInput, PasswordInput, EmailInput, FileInput


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "email",
            "profile_image",
        )

        labels = {
            "username": "아이디",
            "email": "이메일",
            "profile_image": "프로필이미지",
        }

        widgets = {
            "username": TextInput(
                attrs={
                    "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                    "style": "background: transparent;",
                    "placeholder": "아이디를 입력해주세요",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                    "style": "background: transparent;",
                    "placeholder": "이메일을 입력해주세요",
                }
            ),
            "profile_image": FileInput(
                attrs={
                    "style": "background: transparent;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget = forms.widgets.PasswordInput(
            attrs={
                "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                "style": "background: transparent;",
                "placeholder": "비밀번호를 입력해주세요",
            }
        )
        self.fields["password2"].widget = forms.widgets.PasswordInput(
            attrs={
                "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                "style": "background: transparent;",
                "placeholder": "비밀번호를 입력해주세요",
            }
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ("email", "profile_image", "content")
        labels = {
            "email": "이메일",
            "profile_image": "프로필이미지",
            "content": "프로필 소개",
        }

        widgets = {
            "email": EmailInput(
                attrs={
                    "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1 mb-4",
                    "style": "background: transparent;",
                }
            ),
            "profile_image": FileInput(
                attrs={
                    "class": "mb-4",
                    "style": "background: transparent;",
                }
            ),
            "content": TextInput(
                 attrs={
                    "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                    "style": "background: transparent;",
                    "placeholder": "소개를 입력해주세요"
                }
            )
        }


class CustomUserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "아이디"

        self.fields["username"].widget = forms.widgets.TextInput(
            attrs={
                "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                "style": "background: transparent; letter-spacing: -1px;",
                "placeholder": "아이디를 입력해주세요",
            }
        )
        self.fields["password"].widget = forms.widgets.PasswordInput(
            attrs={
                "class": "border-0 border-bottom border-1 border-dark rounded-0 mx-1",
                "style": "background: transparent; letter-spacing: -1px;",
                "placeholder": "비밀번호를 입력해주세요",
            }
        )
