from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from products.models import Product, Image
from django.db.models import Q
from django.views.generic import FormView


def main(request):

    return render(request, "main.html")


def search(request):
    search = Product.objects.all().order_by("-pk")
    q = request.POST.get("q", "")
    if q:
        name = search.filter(name__icontains=q)
        context = {
            "name": name,
            "q": q,
        }
        return render(request, "searched.html", context)
    else:
        return render(request, "searched.html")
