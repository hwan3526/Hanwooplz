from django.db import models

from post.models import Post
from account.models import UserProfile


class Notification(models.Model):
    '''
    type
    0: project apply
    1: answer
    2: comment
    3: like
    '''
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    accept_or_not = models.BooleanField(null=True)
    read_or_not = models.BooleanField(null=True)
