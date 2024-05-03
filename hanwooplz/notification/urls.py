from django.urls import path, include
from notification import views

app_name = 'notification'

urlpatterns = [
    path('send_application/', views.send_application, name='send_application'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('accept_reject_notification/', views.accept_reject_notification, name='accept_reject_notification'),
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]
