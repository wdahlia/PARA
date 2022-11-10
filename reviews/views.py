from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import ReviewForm, CommentForm
from .forms import CommentForm
from .models import Review, Comment
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe


@login_required
def review_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect("reviews:product_detail", product.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/review_form.html", context)


def review_detail(request, product_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    product = Product.objects.get(pk=product_pk)
    context = {
        "review": review,
        "product": product,
        "comment_form": CommentForm(),
        "comments": review.comment_set.all(),
    }
    return render(request, "reviews/review_detail.html", context)
