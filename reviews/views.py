from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Product, Comment
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
from django.views.generic import ListView, TemplateView, DetailView


@login_required
def review_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == "POST":
        tags = request.POST.get("tag", "").split(",")
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            for tag in tags:
                tag = tag.strip()
                if tag != "":
                    review.tags.add(tag)
            review.save()
            return redirect("products:detail", product.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/review_create.html", context)


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


@login_required
def review_delete(request, product_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("products:detail", product_pk)
    return redirect("products:detail", product_pk)


@login_required
def review_update(request, product_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("reviews:review_detail", product_pk, review_pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            "review_form": review_form,
        }
        return render(request, "reviews/review_update.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("products:detail", product_pk)


def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.review = review
                comment.user = request.user
                comment.save()
                context = {
                    "review_pk": review_pk,
                    "comment_pk": comment.pk,
                    "content": comment.content,
                    "userName": comment.user.username,
                }

                return JsonResponse(context)
        else:
            return HttpResponse(status=403)
    else:
        return redirect("accounts:login")


@login_required
def comment_delete(request, product_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()

    data = {}
    return JsonResponse(data)


class TagCloudTV(TemplateView):
    template_name = "taggit/taggit_cloud.html"


class TaggedObjectLV(ListView):
    template_name = "taggit/taggit_post_list.html"
    model = Review

    def get_queryset(self):
        return Review.objects.filter(tags__name=self.kwargs.get("tag"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tagname"] = self.kwargs["tag"]
        return context
