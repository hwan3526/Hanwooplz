from django.urls import path

from index import views

app_name = 'comment'

urlpatterns = [
    path("api/post/<int:post_id>/comments/", views.CommentList.as_view(), name="comment_list"),
    path("api/comments/<int:comment_id>/", views.CommentDetail.as_view(), name="comment_detail"),
    path("api/comment/<int:pk>/like/", views.CommentLikeView.as_view(), name="comment_like"),
]
