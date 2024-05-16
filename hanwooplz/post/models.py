from django.db import models
from django.contrib.postgres.fields import ArrayField
from tinymce.models import HTMLField

from account.models import UserProfile


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
