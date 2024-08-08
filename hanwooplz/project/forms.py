from django import forms

from project.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['start_date', 'end_date', 'target_members', 'tech_stack', 'ext_link']
