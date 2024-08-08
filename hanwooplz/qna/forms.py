from django import forms

from qna.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['keyword']
