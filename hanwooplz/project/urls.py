from django.urls import path

from project import views

app_name = 'project'

urlpatterns = [
    path('project/', views.list, name='list'),
    path('project/<int:project_id>', views.read, name='read'),
    path('project/write', views.write, name='write'),
    path('project/edit/<int:project_id>', views.write, name='edit'),
    path('update-status', views.update_status, name='update_status'),
]
