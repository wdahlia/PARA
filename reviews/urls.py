from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("review_create/", views.review_create, name="review_create"),
    path("<int:review_pk>/review_detail/", views.review_detail, name="review_detail"),
    path("<int:review_pk>/review_delete/", views.review_delete, name="review_delete"),
    path("<int:review_pk>/review_update/", views.review_update, name="review_update"),
]
