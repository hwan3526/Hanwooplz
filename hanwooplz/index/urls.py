from django.urls import path

from index import views

app_name = 'index'

urlpatterns = [
    path('', views.main, name='main'),
    path('index',views.index, name='index'),
]
