from django import forms

from qna.models import PostQuestion


class PostQuestionForm(forms.ModelForm):
    class Meta:
        model = PostQuestion
        fields = ['keyword']
