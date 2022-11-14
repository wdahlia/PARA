from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("<int:pk>/", views.detail, name="detail"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("update/", views.update, name="update"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    # 이메일 회원가입: activate (user 정보 복호화 및 인증 및 로그인)
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
]
