from django import forms

from portfolio.models import Portfolio


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['start_date','end_date','tech_stack','ext_link','members']
