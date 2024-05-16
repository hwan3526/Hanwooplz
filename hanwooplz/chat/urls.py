from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('chat/<int:room_number>/<int:receiver_id>', views.current_chat, name='chat'),
    path('chat-msg/<int:room_number>', views.chat_msg, name='chat_msg'),
]
