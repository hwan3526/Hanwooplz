from django.db import models

from post.models import PostPnP


class PostPortfolio(PostPnP):
    members = models.IntegerField(default=1)
