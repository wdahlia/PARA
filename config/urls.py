"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


################## chat ######################
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser
from typing import List

UserModel = get_user_model()
#################################################

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views


class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        return UserModel.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context["object_list"]

        data = [{"username": user.get_username(), "pk": str(user.pk)} for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)


################## chat ######################


urlpatterns = [
    path("chat/", include("chat.urls")),
    ################## chat ######################
    path("", include("django_private_chat2.urls")),
    path("users/", UsersListView.as_view(), name="users_list"),
    path(
        "chat2/",
        login_required(TemplateView.as_view(template_name="chat2base.html")),
        name="home",
    ),
    ##############################################
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("reviews/", include("reviews.urls")),
    path("admin/", admin.site.urls),
    path("", views.main, name="main"),
    path("", include("allauth.urls")),
    path("search/", views.search, name="search"),
    path("cart/", include("cart.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
