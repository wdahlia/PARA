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
    name = search.filter(name__icontains=q)  # 검색된 상품
    if q and len(name) != 0:  # 검색결과가 있으면
        # print(len(name))
        dicts = {}  # 상품정보와 사진을 담을 예정
        for n in name:  # 각 상품에
            image = Image.objects.filter(product_id=n.id)[0]  # 첫번째 이미지를 받고
            dicts[n] = image  # 상품과 이미지를 딕셔너리형태로 저장
        dicts_len = len(dicts)  # 상품의 개수를 알기 위해 결과의 길이를 출력
        context = {
            "dicts": dicts,
            "dicts_len": dicts_len,
            "name": name,
            "q": q,
        }
        return render(request, "searched.html", context)
    else:
        products = Product.objects.all()  # 모든 상품을 가져와서
        products_list = []
        for p in products:
            products_list.append(p.pk)  # 상품의 pk를 저장
        result = random.sample(products_list, 10)  # 랜덤으로 10개의 pk를 출력
        dicts = {}  # 삼품과 이미지 담을 곳
        for i in result:
            product = Product.objects.get(pk=i)  # 랜덤으로 뽑은 pk의 상품을 가져왔다.
            image = Image.objects.filter(product_id=i)[0]  # 그 상품의 첫번째 이미지 가져옴
            dicts[product] = image  # 딕셔너리에 저장
        data = {"dicts": dicts}
        return render(request, "searched.html", data)
