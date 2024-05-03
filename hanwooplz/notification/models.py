from django.db import models

from post.models import Post
from account.models import UserProfile

# Create your models here.


class Notifications(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='user')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,related_name='prj_sender')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accept_or_not = models.BooleanField(null=True)
    read_or_not = models.BooleanField(default=False)
