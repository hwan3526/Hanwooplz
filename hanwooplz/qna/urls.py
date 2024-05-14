from django.urls import path

from qna import views

app_name = 'qna'

urlpatterns = [
    path('qna/', views.qna_list, name='qna_list'),
    path('qna/<int:post_question_id>', views.qna_read, name='qna_read'),
    path('qna/write/question', views.qna_write_question, name='qna_write_question'),
    path('qna/write/question/<int:post_question_id>', views.qna_write_question, name='qna_edit_question'),
    path('qna/write/answer/<int:post_question_id>', views.qna_write_answer, name='qna_write_answer'),
    path('qna/write/answer/<int:post_question_id>/<int:post_answer_id>', views.qna_write_answer, name='qna_edit_answer'),
    path('qna/like/<int:post_question_id>', views.like, name='question_like'),
    path('qna/like/<int:post_question_id>/<int:answer_id>', views.like, name='answer_like'),
]
