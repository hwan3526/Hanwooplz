from django.db import models
from django.contrib.postgres.fields import ArrayField

from account.models import UserProfile
from post.models import PostQnA


class PostQuestion(PostQnA):
    keyword = ArrayField(models.CharField(max_length=20))
    like = models.ManyToManyField(UserProfile, through='QuestionLike')


class PostAnswer(PostQnA):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    like = models.ManyToManyField(UserProfile, through='AnswerLike')


class QuestionLike(models.Model):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    answer = models.ForeignKey(PostAnswer, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
