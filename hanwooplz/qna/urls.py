from django.urls import path

from qna import views

app_name = 'qna'

urlpatterns = [
    path('qna/', views.list, name='list'),
    path('qna/<int:question_id>', views.read, name='read'),
    path('qna/write-question', views.write_question, name='write_question'),
    path('qna/edit-question/<int:question_id>', views.write_question, name='edit_question'),
    path('qna/write-answer/<int:question_id>', views.write_answer, name='write_answer'),
    path('qna/edit-answer/<int:question_id>/<int:answer_id>', views.write_answer, name='edit_answer'),
    path('qna/like/<int:question_id>', views.like, name='like_question'),
    path('qna/like/<int:question_id>/<int:answer_id>', views.like, name='like_answer'),
]
