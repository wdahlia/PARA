from django.shortcuts import render, redirect
from .models import Image, Product, Category
from reviews.models import Review
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
        review_ave += review.grade
        cnt += 1
    if cnt == 0:
        review_ave = "평가없음"
    else:
        review_ave = round((review_ave / cnt), 2)
    context = {
        "products": products,
        "images": images,
        "reviews": reviews,
        "review_ave": review_ave,
    }
    response = render(request, "products/detail.html", context)
    products.hits += 1
    products.save()

    return response


def category(request, category_pk):
    c = Category.objects.get(sort=category_pk)
    products = Product.objects.filter(category_id=c)
    # images = Image.objects.filter()
    img_dict = {}
    for product in products:

        img = Image.objects.filter(product_id=product.id)[0]  # 프로덕트 ID에 해당하는 0번째 이미지 객체 가져옴

        img_dict[product.id] = img
    # print(img_dict)
    # gender = Product.objects.filter(gender=gender)
    # print(images)
    context = {
        "img_dict": img_dict,
        "products": products,
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
    product = Product.objects.get(pk=pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if product.like_users.filter(id=request.user.id).exists():
    if request.user in product.like_users.all():
        # 좋아요 삭제하고
        product.like_users.remove(request.user)
    else:
        # 좋아요 추가하고
        product.like_users.add(request.user)
        # 상세 페이지로 redirect
    return redirect("products:detail", pk)
