from django.urls import path
from .consumers import EchoConsumerText, EchoConsumerJSON, GetUserInfo

websocket_urlpatterns = [
    path("ws/api/echo-text/", EchoConsumerText.as_asgi()),
    path("ws/api/echo-json/", EchoConsumerJSON.as_asgi()),
    path("ws/api/get-user-info/", GetUserInfo.as_asgi()),
]