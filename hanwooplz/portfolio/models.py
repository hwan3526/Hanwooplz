from django.db import models

from post.models import PnP


class Portfolio(PnP):
    members = models.IntegerField(default=1)
