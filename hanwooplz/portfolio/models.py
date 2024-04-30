from django.db import models

from post.models import PostPnP

# Create your models here.


class PostPortfolio(PostPnP):
    members = models.IntegerField(default=1)
