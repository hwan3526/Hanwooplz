from django.urls import path, include
from portfolio import views

app_name = 'portfolio'

urlpatterns = [    
    path("portfolio", views.portfolio_list, name="portfolio_list"),
    path("portfolio/<int:post_portfolio_id>", views.portfolio, name="portfolio_read"),
    path("portfolio/write", views.write_portfolio, name="portfolio_write"),
    path("portfolio/write/<int:post_portfolio_id>", views.write_portfolio, name="portfolio_edit"),
]
