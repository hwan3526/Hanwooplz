from django.db import models

from account.models import UserProfile


class ChatRoom(models.Model):
    members = models.ManyToManyField(UserProfile, through='ChatRoomMembers')
    created_at = models.DateTimeField(auto_now_add=True)


class ChatRoomMembers(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    members = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    read_or_not = models.ManyToManyField(UserProfile, through='ChatMessageReadOrNot')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessageReadOrNot(models.Model):
    chatmessage = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
