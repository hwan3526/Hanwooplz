from django import forms
from project.models import PostProject


class PostProjectForm(forms.ModelForm):
    class Meta:
        model = PostProject
        fields = ['start_date', 'end_date', 'target_members', 'tech_stack', 'ext_link']
