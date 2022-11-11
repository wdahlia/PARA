from django.shortcuts import render
from .models import Image, Product

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
    # template에 객체 전달
    context = {
        "products": products,
        "images": images,
    }
    return render(request, "products/detail.html", context)
