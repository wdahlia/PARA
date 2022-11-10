from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import JsonResponse

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
                user = form.save()
                auth_login(request, user)
                return redirect("accounts:index")
        else:
            form = CustomUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/signup.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {"user": user}
    return render(request, "accounts/detail.html", context)


def login(request):
    # if request.user.is_anonymous:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
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
