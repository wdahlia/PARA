from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import CustomUserAuthenticationForm
from django.http import JsonResponse

from django.contrib import messages  # 알림 메세지

# 이메일 회원가입 관련 메서드
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

# tokens.py 가져오기
from .tokens import account_activation_token

# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    # 이미 로그인된 사람은 accounts:index 로 보내기
    if request.user.is_authenticated:
        return redirect("accounts:index")
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                # 👇👇 바로 로그인 되도록 새로 추가된 코드
                user = form.save(commit=False)  # 바로 저장 안 하고 user 객체 받아옴
                user.is_active = (
                    False  # user의 is_active(인증 여부)를 False로 저장 (default : True)
                )
                user.save()  # user 정보 저장
                activateEmail(
                    request, user, form.cleaned_data.get("email")
                )  # 이메일 보내기 함수 만들어서 정보 전달 (request, user 객체, 검증된 데이터["email"])
                return redirect("accounts:index")
            else:
                for err in list(form.errors.values()):
                    messages.error(request, err)
        else:
            form = CustomUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/signup.html", context)


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "accounts/template_activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.",
        )
    else:
        messages.error(
            request,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        auth_login(request, user)
        return redirect("accounts:index")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("accounts:index")


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {"user": user}
    return render(request, "accounts/detail.html", context)


def login(request):
    # if request.user.is_anonymous:
    if request.method == "POST":
        form = CustomUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = CustomUserAuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


# else:
#     return redirect("accounts:index")


def logout(request):
    auth_logout(request)
    return redirect("accounts:index")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


def follow(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(pk=pk)
        if user != request.user:
            if user.followers.filter(pk=request.user.pk).exists():
                user.followers.remove(request.user)
                is_followed = False
            else:
                user.followers.add(request.user)
                is_followed = True
            follow_user = user.followers.filter(pk=request.user.pk)
            following_user = user.followings.filter(pk=request.user.pk)
            follow_user_list = []
            following_user_list = []
            for follow in follow_user:
                follow_user_list.append(
                    {
                        "pk": follow.pk,
                        "username": follow.username,
                    }
                )
            for following in following_user:
                following_user_list.append(
                    {
                        "pk": following.pk,
                        "username": following.username,
                    }
                )
            context = {
                "is_followed": is_followed,
                "follow_user": follow_user_list,
                "following_user": following_user_list,
                "followers_count": user.followers.count(),
                "followings_count": user.followings.count(),
            }
            return JsonResponse(context)
        return redirect("accounts:detail", user.username)
    return redirect("accounts:login")
