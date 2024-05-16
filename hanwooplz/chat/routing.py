from django.urls import re_path

from chat.customers import ChatConsumer, ChatListConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_number>\d+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat_list/$', ChatListConsumer.as_asgi()),
]
