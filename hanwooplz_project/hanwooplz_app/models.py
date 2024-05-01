from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from tinymce.models import HTMLField

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='Untitled')
    content = HTMLField()

class PostPnP(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    tech_stack = ArrayField(models.CharField(max_length=20))
    ext_link = models.URLField()

    class Meta:
        abstract = True

class PostQnA(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class PostQuestion(PostQnA):
    keyword = ArrayField(models.CharField(max_length=20))
    like = models.ManyToManyField(UserProfile, through="QuestionLike")

class PostAnswer(PostQnA):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    like = models.ManyToManyField(UserProfile, through="AnswerLike")

class QuestionLike(models.Model):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class AnswerLike(models.Model):
    answer = models.ForeignKey(PostAnswer, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="comments_written")
    content = models.TextField()
    like = models.ManyToManyField(UserProfile, through="CommentLike")
    created_at = models.DateTimeField(auto_now_add=True)

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

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

class Notifications(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='user')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,related_name='prj_sender')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accept_or_not = models.BooleanField(null=True)
    read_or_not = models.BooleanField(default=False)
