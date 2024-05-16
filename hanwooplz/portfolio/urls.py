from django.urls import path

from portfolio import views

app_name = 'portfolio'

urlpatterns = [    
    path('portfolio', views.portfolio_list, name='portfolio_list'),
    path('portfolio/<int:post_portfolio_id>', views.portfolio_read, name='portfolio_read'),
    path('portfolio/write', views.portfolio_write, name='portfolio_write'),
    path('portfolio/write/<int:post_portfolio_id>', views.portfolio_write, name='portfolio_edit'),
]
