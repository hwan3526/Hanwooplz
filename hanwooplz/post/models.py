from django.db import models
from tinymce.models import HTMLField

from account.models import UserProfile


class Post(models.Model):
    '''
    category
    - 0: portfolio
    - 1: project
    - 2: question
    - 3: answer
    '''
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50, default='Untitled')
    content = HTMLField()
    category = models.IntegerField()


class PnP(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    tech_stack = models.TextField()
    ext_link = models.URLField()

    class Meta:
        abstract = True


class QnA(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True
