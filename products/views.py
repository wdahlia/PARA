from django.shortcuts import render, redirect, get_object_or_404
from .models import Image, Product, Category
from reviews.models import Review
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random

# Create your views here.
def index(request):
    # images = Image.objects.order_by("-pk").
    images = Image.objects.all()
    products = Product.objects.all()
    context = {
        "products": products,
        "images": images,
    }
    return render(request, "products/index.html", context)


def detail(request, pk):
    # 특정 글을 가져온다.
    products = Product.objects.get(pk=pk)
    images = Image.objects.filter(product_id=pk)
    reviews = Review.objects.filter(product_id=pk)

    # template에 객체 전달

    review_ave = 0
    cnt = 0
    for review in reviews:
        review_ave += int(review.grade)
        cnt += 1
    if cnt == 0:
        review_ave = "평가없음"
        star = ""
    else:
        review_ave = round((review_ave / cnt), 2)
    if review_ave != "평가없음":
        if review_ave > 4.8:
            star = 5.0
        elif 4.8 >= review_ave > 4.3:
            star = 4.5
        elif 4.3 >= review_ave > 3.8:
            star = 4.0
        elif 3.8 >= review_ave > 3.3:
            star = 3.5
        elif 3.3 >= review_ave > 2.8:
            star = 3.0
        elif 2.8 >= review_ave > 2.3:
            star = 2.5
        elif 2.3 >= review_ave > 1.8:
            star = 2
        elif 1.8 >= review_ave > 1.3:
            star = 1.5
        elif 1.3 >= review_ave > 0.8:
            star = 1.0
        elif 0.8 >= review_ave > 0:
            star = 0.5
    context = {
        "products": products,
        "images": images,
        "reviews": reviews,
        "review_ave": review_ave,
        "star": star,
    }
    response = render(request, "products/detail.html", context)
    products.hits += 1
    products.save()

    return response


def category(request, category_pk):
    c = Category.objects.get(sort=category_pk)
    products = Product.objects.filter(category_id=c)
    # images = Image.objects.filter()
    # 전체
    img_dict = {}
    for product in products:

        img = Image.objects.filter(product_id=product.id)[0]  # 프로덕트 ID에 해당하는 0번째 이미지 객체 가져옴

        img_dict[product.id] = img
    # print(img_dict)
    # gender = Product.objects.filter(gender=gender)
    # print(images)

    # 남자 인 경우 
    products_man = products.filter(gender='MAN')
    dicts1 = {}
    for i in products_man:
        product = Product.objects.get(pk=i.pk)
        image = Image.objects.filter(product_id=i.pk)[0]
        dicts1[product] = image

    # 여자 인 경우
    products_woman = products.filter(gender='WOMAN')
    dicts2 = {}
    for j in products_woman:
        product = Product.objects.get(pk=j.pk)
        image = Image.objects.filter(product_id=j.pk)[0]
        dicts2[product] = image

    context = {
        "img_dict": img_dict,
        "products": products,
        "category": category_pk,
        "man_clothes" : products_man,
        "dicts1": dicts1,
        "woman_clothes" : products_woman,
        "dicts2": dicts2,  
        # "images": images,
        # "gender": gender,
    }
    return render(request, "products/category.html", context)


# def category(request, category_id):
#     categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     products = Product.objects.filter(category=category).order_by("pub_date")
#     lank_products = Product.objects.filter(category=category).order_by("-hit")[:4]
#     paginator = Paginator(products, 5)
#     page = request.GET.get("page")
#     try:
#         products = paginator.page(page)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)
#     print(categories)
#     context = {
#         "lank_products": lank_products,
#         "products": products,
#         "category": category,
#         "categories": categories,
#     }
#     return render(request, "products/category.html", context)
@login_required
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
            is_liked = False
        else:
            product.like_users.add(request.user)
            is_liked = True
        context = {
            "is_liked": is_liked,
            "likeCount": product.like_users.count(),
        }
        return JsonResponse(context)
    return redirect("accounts:login")


def bestsellers(request):
    products = Product.objects.order_by("-hits")[:12]
    products_list = []
    for p in products:
        products_list.append(p.pk)
    result = products_list
    dicts = {}
    for i in result:
        product = Product.objects.get(pk=i)
        image = Image.objects.filter(product_id=i)[0]
        dicts[product] = image
    data = {"dicts": dicts}
    return render(request, "products/bestsellers.html", data)
