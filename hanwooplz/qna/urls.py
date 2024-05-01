from django.urls import path
from qna import views

app_name = 'qna'

urlpatterns = [
    path("qna/", views.question_list, name="question_list"),
    path("qna/<int:post_question_id>", views.question, name="question_read"),
    path("qna/question/write", views.write_question, name="question_write"),
    path("qna/question/write/<int:post_question_id>", views.write_question, name="question_edit"),
    path("qna/answer/<int:post_question_id>", views.write_answer, name="answer_write"),
    path("qna/answer/<int:post_question_id>/<int:post_answer_id>", views.write_answer, name="answer_edit"),
    path("qna/like/<int:post_question_id>", views.like, name="question_like"),
    path("qna/like/<int:post_question_id>/<int:answer_id>", views.like, name="answer_like"),
]
