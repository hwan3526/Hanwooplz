from django.urls import path

from portfolio import views

app_name = 'portfolio'

urlpatterns = [    
    path('portfolio', views.list, name='list'),
    path('portfolio/<int:portfolio_id>', views.read, name='read'),
    path('portfolio/write', views.write, name='write'),
    path('portfolio/edit/<int:portfolio_id>', views.edit, name='edit'),
    path('portfolio/delete/<int:portfolio_id>', views.delete, name='delete'),
]
