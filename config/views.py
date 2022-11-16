from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from products.models import Product, Image
from django.db.models import Q
from django.views.generic import FormView
import random

def main(request):

    return render(request, "main.html")


def search(request):
    search = Product.objects.all().order_by("-pk")
    q = request.POST.get("q", "")
    name = search.filter(name__icontains=q)
    if q and len(name) != 0:
        # print(len(name))
        dicts={}
        for n in name:
            image = Image.objects.filter(product_id = n.id)[0]
            dicts[n]=image
        dicts_len = len(dicts)
        context = {
            "dicts":dicts, 
            'dicts_len':dicts_len,
            "name": name,
            "q": q,
        }
        return render(request, "searched.html", context)
    else:
        products = Product.objects.all()
        products_list = []
        for p in products:
            products_list.append(p.pk)
        result = random.sample(products_list,10)
        dicts={}
        for i in result:
            product = Product.objects.get(pk=i)
            image = Image.objects.filter(product_id = i)[0]
            dicts[product]=image
        data = {
            'dicts':dicts
        }
        return render(request, "searched.html",data)
