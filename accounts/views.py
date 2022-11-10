from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from .models import User
import json


def login(request):
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


def logout(request):
    auth_logout(request)
    return redirect("accounts:index")


def detail(request, pk):
    user = User.objects.get(pk=pk)
    profile_image = user.profile_image
    username = user.username
    context = {
        "user": user,
        "profile_image": profile_image,
        "username": username,
    }
    return render(request, "accounts/detail.html", context)


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
            print(follow_user)
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
        return redirect("accounts:userpage", user.username)
    return redirect("accounts:login")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def update(request, pk):
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
