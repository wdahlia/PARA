from django.shortcuts import render
import json
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
from django.views.generic import ListView, TemplateView


@login_required
def review_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == "POST":
        tags = request.POST.get("tags", "").split(",")
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            for tag in tags:
                tag = tag.strip()
                if tag != "":
                    review.tags.add(tag)
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
            tags = request.POST.get("tags", "").split(",")
            review.tags.clear()
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = request.user
                form.save()
                for tag in tags:
                    tag = tag.strip()
                    if tag != "":
                        review.tags.add(tag)
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

# 분기처리는 result 0이면 댓글 아니면 대댓글
#  if result:
#         print(request.POST['parent'])
# elif  result == 0 : print(0)
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    result = request.POST['parent']

    if request.method == "POST": # POST요청이고
        if request.user.is_authenticated: # 로그인된 상태면
                # 댓글일 때
            if  int(result) == 0 :
                comment_form = CommentForm(request.POST) # POST으로 요청온 정보를 받아서
                if comment_form.is_valid(): # 유효성 검사하고
                    comment = comment_form.save(commit=False) # 저장 멈춰
                    # 외래키 입력
                    comment.review = review 
                    comment.user = request.user
                    # 저장
                    comment.save()
                    
                    context = {
                        "review_pk": review_pk,
                        "comment_pk": comment.pk,
                        "content": comment.content,
                        "userName": comment.user.username,
                        "comment_image" : comment.user.profile_image.url
                    }
                    return JsonResponse(context)
                
            elif int(result) > 0 :
                comment_form = CommentForm(request.POST) # POST으로 요청온 정보를 받아서
                if comment_form.is_valid(): # 유효성 검사하고
                    comment = comment_form.save(commit=False) # 저장 멈춰
                    # 외래키 입력
                    comment.review = review 
                    comment.user = request.user
                    comment.parent_id = result
                    # 저장
                    comment.save()
                    image = 0
                    if request.user.profile_image:
                        image = request.user.profile_image.url
                        
                    context = {
                        "review_pk": review_pk,
                        "comment_pk": comment.pk,
                        "content": comment.content,
                        "userName": comment.user.username,
                        'image':image,
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
        response = Review.objects.filter(tags__name=self.kwargs.get("tag")).select_related(
            "product"
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tagname"] = self.kwargs["tag"]
        return context
