from django import forms

from portfolio.models import PostPortfolio


class PostPortfolioForm(forms.ModelForm):
    class Meta:
        model = PostPortfolio
        fields = ['start_date','end_date','tech_stack','ext_link','members']
