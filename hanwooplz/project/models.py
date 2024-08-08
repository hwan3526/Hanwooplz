from django.db import models

from account.models import UserProfile
from post.models import PnP


class Project(PnP):
    '''
    status
    - 0: 모집중단
    - 1: 모집중
    - 2: 모집완료
    '''
    status = models.IntegerField(default=1)
    members = models.ManyToManyField(UserProfile, through='ProjectMembers')
    target_members = models.IntegerField(default=1)


class ProjectMembers(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    members = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
