from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('register', views.register, name='register'),
    path('find-id', views.find_id, name='find_id'),
    path('find-pw', views.find_pw, name='find_pw'),
    path('found-pw', views.found_pw, name='found_pw'),
    path('myinfo/<int:user_id>', views.myinfo, name='myinfo'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('change-password', views.change_password, name='change_password'),
]
