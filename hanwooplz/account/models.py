from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    '''
    User model-builtin column with AbstractUser class
    - username: ID
    - password: PW
    - email: Email
    '''
    first_name = None
    last_name = None
    
    # Custom column
    full_name = models.CharField(max_length=7)
    job = models.CharField(max_length=20)
    tech_stack = models.TextField()
    career = models.IntegerField(default=0)
    career_detail = models.TextField()
    introduction = models.TextField()
    github_link = models.URLField(blank=True,default='')
    linkedin_link = models.URLField(blank=True,default='')
    profile_image = models.ImageField(upload_to='static/profile_image', blank=True, default='')
