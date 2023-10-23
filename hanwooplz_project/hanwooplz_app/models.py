from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class user_profile(AbstractUser):
    '''
    User model-builtin column with AbstractUser class
    - ID: username
    - PW: password
    - Email: email
    '''
    first_name = None
    last_name = None
    
    # custom column
    full_name = models.CharField(max_length=6)
    job = models.CharField(max_length=50)
    tech_stack = ArrayField(models.CharField(max_length=20))
    career = models.IntegerField(default=0)
    career_detail = models.TextField() # could be modified
    introduction = models.TextField()

class post(models.Model):
    author = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='Untitled')
    content = models.TextField()

class post_pnp(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    tech_stack = ArrayField(models.CharField(max_length=20))
    ext_link = models.URLField()

    class Meta:
        abstract = True

class post_portfolio(post_pnp):
    members = models.IntegerField(default=1)

class post_project(post_pnp):
    status = models.IntegerField(default=1)
    '''
    - 모집중단: 0
    - 모집중: 1
    - 모집완료: 2
    '''
    members = models.ManyToManyField(user_profile, through='project_members')

class project_members(models.Model):
    project = models.ForeignKey(post_project, on_delete=models.CASCADE)
    members = models.ForeignKey(user_profile, on_delete=models.CASCADE)

class post_qna(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)

    class Meta:
        abstract = True

class post_question(post_qna):
    keyword = ArrayField(models.CharField(max_length=20))

class post_answer(post_qna):
    question = models.ForeignKey(post_question, on_delete=models.CASCADE)

class comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    author = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    content = models.TextField()
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

# would be modified

class chat_room(models.Model):
    # post = models.ForeignKey(post, on_delete=models.CASCADE)
    sender = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='buyer')
    receiver = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)


class chat_messages(models.Model):  
    chat_room = models.ForeignKey(chat_room, on_delete=models.CASCADE)
    sender = models.ForeignKey(user_profile, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(user_profile, on_delete=models.CASCADE, null=True, related_name='receiver')
    message = models.CharField(max_length=500)
    read_or_not = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat_uuid = models.UUIDField(editable=False, unique=True, null=True)
