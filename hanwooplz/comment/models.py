from django.db import models

from post.models import Post
from account.models import UserProfile


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments_written')
    content = models.TextField()
    like = models.ManyToManyField(UserProfile, through='CommentLike')
    created_at = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
