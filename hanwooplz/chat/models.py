from django.db import models

from account.models import UserProfile
from post.models import Post

# Create your models here.


class ChatRoom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessages(models.Model):  
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='receiver')
    message = models.CharField(max_length=500)
    read_or_not = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat_uuid = models.UUIDField(editable=False, unique=True, null=True)
