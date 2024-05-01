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

    # comment_views.py
    path("api/post/<int:post_id>/comments/", comment_views.CommentList.as_view(), name="comment_list"),
    path("api/comments/<int:comment_id>/", comment_views.CommentDetail.as_view(), name="comment_detail"),
    path("api/comment/<int:pk>/like/", comment_views.CommentLikeView.as_view(), name="comment_like"),
    path("question-test/", comment_views.question_test, name="question_test"),
    path("post-test/", comment_views.post_test, name="post_test"),
    
    # chat_views.py
    path('chat/<int:room_number>/<int:receiver_id>', chat_views.current_chat, name='chat'),
    path('chat-msg/<int:room_number>', chat_views.chat_msg, name='chat_msg'),
]
