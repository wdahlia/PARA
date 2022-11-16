from django.urls import path, include
from chat import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "chat"

urlpatterns = [
    path("", views.chatPage, name="chat-page"),
    path("main", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
