from django.db import models

from account.models import UserProfile
from post.models import QnA


class Question(QnA):
    keyword = models.TextField()
    like = models.ManyToManyField(UserProfile, through='QuestionLike')


class Answer(QnA):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like = models.ManyToManyField(UserProfile, through='AnswerLike')


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
