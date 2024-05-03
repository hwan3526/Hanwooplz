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

class Notifications(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='user')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,related_name='prj_sender')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accept_or_not = models.BooleanField(null=True)
    read_or_not = models.BooleanField(default=False)
