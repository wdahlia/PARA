from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("<int:product_pk>/review_create/", views.review_create, name="review_create"),
    path(
        "<int:product_pk>/<int:review_pk>/review_detail/",
        views.review_detail,
        name="review_detail",
    ),
    path(
        "<int:product_pk>/<int:review_pk>/review_delete/",
        views.review_delete,
        name="review_delete",
    ),
    path(
        "<int:product_pk>/<int:review_pk>/review_update/",
        views.review_update,
        name="review_update",
    ),
    path(
        "<int:review_pk>/review_detail/comments/",
        views.comment_create,
        name="comment_create",
    ),
    path(
        "<int:product_pk>/<int:review_pk>/review_detail/comments/<int:comment_pk>/comment_delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("tag/", views.TagCloudTV.as_view(), name="tag_cloud"),
    path("tag/<str:tag>/", views.TaggedObjectLV.as_view(), name="tagged_object_list"),
]
