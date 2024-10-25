from django.urls import path

from qna import views

app_name = 'qna'

urlpatterns = [
    path('qna/', views.list, name='list'),
    path('qna/<int:question_id>', views.read, name='read'),
    path('qna/write-question', views.write_question, name='write_question'),
    path('qna/edit-question/<int:question_id>', views.edit_question, name='edit_question'),
    path('qna/delete-question/<int:question_id>', views.delete_question, name='delete_question'),
    path('qna/write-answer/<int:question_id>', views.write_answer, name='write_answer'),
    path('qna/edit-answer/<int:answer_id>', views.edit_answer, name='edit_answer'),
    path('qna/delete-answer/<int:answer_id>', views.delete_answer, name='delete_answer'),
    path('qna/like-question/<int:question_id>', views.like_question, name='like_question'),
    path('qna/like-answer/<int:answer_id>', views.like_answer, name='like_answer'),
]
