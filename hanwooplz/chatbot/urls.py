from django.urls import path
from chatbot import views

app_name = 'chatbot'

urlpatterns = [
    path('execute_chatbot/', views.execute_chatbot, name='execute_chatbot'),
]
