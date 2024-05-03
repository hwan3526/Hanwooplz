from django.urls import path, include
from .views import views, chat_views, comment_views, question_views, project_views, portfolio_views


app_name = 'hanwooplz_app'

urlpatterns = [
    path('write/',views.write, name='write'),
    path("post/", views.post, name="post"),
    path("post-list/", views.post_list, name="post_list"),
]
