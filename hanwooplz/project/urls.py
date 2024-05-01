from django.urls import path
from project import views

app_name = 'project'

urlpatterns = [
    path("project/", views.project_list, name="project_list"),
    path("project/<int:post_project_id>", views.project, name="project_read"),
    path("project/write", views.write_project, name="project_write"),
    path("project/write/<int:post_project_id>", views.write_project, name="project_edit"),
    path("update-status/", views.update_views, name="update_status"),
]
