from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

# Create your views here.
def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    context = {"room_name": room_name}
    return render(request, "chat/room.html", context)


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    context = {}
    return render(request, "chat/chatPage.html", context)
