from django.urls import path

from project import views

app_name = 'project'

urlpatterns = [
    path('project/', views.project_list, name='project_list'),
    path('project/<int:post_project_id>', views.project_read, name='project_read'),
    path('project/write', views.project_write, name='project_write'),
    path('project/write/<int:post_project_id>', views.project_write, name='project_edit'),
    path('update-status', views.update_views, name='update_status'),
]
