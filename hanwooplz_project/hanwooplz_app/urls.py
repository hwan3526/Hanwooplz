from django.urls import path, include
from .views import views, chat_views, comment_views, question_views, project_views, portfolio_views


app_name = 'hanwooplz_app'

urlpatterns = [
    path('write/',views.write, name='write'),
    path("post/", views.post, name="post"),
    path("post-list/", views.post_list, name="post_list"),
    path('execute_chatbot/', views.execute_chatbot, name='execute_chatbot'),
    path('send_application/', views.send_application, name='send_application'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('accept_reject_notification/', views.accept_reject_notification, name='accept_reject_notification'),
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),

    # chat_views.py
    path('chat/<int:room_number>/<int:receiver_id>', chat_views.current_chat, name='chat'),
    path('chat-msg/<int:room_number>', chat_views.chat_msg, name='chat_msg'),
]
