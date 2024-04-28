from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class UserProfile(AbstractUser):
    '''
    User model-builtin column with AbstractUser class
    - ID: username
    - PW: password
    - Email: email
    '''
    first_name = None
    last_name = None
    
    # Custom column
    full_name = models.CharField(max_length=6)
    job = models.CharField(max_length=50)
    tech_stack = ArrayField(models.CharField(max_length=20))
    career = models.IntegerField(default=0)
    career_detail = models.TextField()
    introduction = models.TextField()
    github_link = models.URLField(blank=True,default='')
    linkedin_link = models.URLField(blank=True,default='')
    user_img = models.ImageField(upload_to="user_img", default=None, null=True)
