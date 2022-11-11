from django.shortcuts import render
from .models import Image, Product

# Create your views here.
def index(request):
    # images = Image.objects.order_by("-pk").
    images = Image.objects.all()
    products = Product.objects.all()
    print(images.values)

    context = {
        "products": products,
        "images": images,
    }
    return render(request, "products/index.html", context)
