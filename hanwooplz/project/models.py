from django.db import models

from account.models import UserProfile
from post.models import PostPnP

# Create your models here.


class PostProject(PostPnP):
    status = models.IntegerField(default=1)
    '''
    - 모집중단: 0
    - 모집중: 1
    - 모집완료: 2
    '''
    members = models.ManyToManyField(UserProfile, through='ProjectMembers')
    target_members = models.IntegerField(default=1)


class ProjectMembers(models.Model):
    project = models.ForeignKey(PostProject, on_delete=models.CASCADE)
    members = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
