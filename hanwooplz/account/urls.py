from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('find-id', views.find_id, name='find_id'),
    path('find-pw', views.find_pw, name='find_pw'),
    path('@<str:username>', views.user_info, name='user_info'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('change-password', views.change_password, name='change_password'),
]
