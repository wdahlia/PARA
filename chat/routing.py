from django.urls import path, include, re_path
from chat.consumers import ChatConsumer, ChatConsumer2

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer2.as_asgi()),
]
