from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from ..forms import *
from ..models import *
from ..serializers import *
import json
import openai
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm


# Create your views here.

# 게시글 작성 화면
def write(request):
    return render(request, 'write.html')

def get_posts_by_category(request):
    category = request.GET.get('category')
    if category == 'post':
        posts = Post.objects.all()  # Post 모델의 게시물을 가져옵니다.
    elif category == 'postportfolio':
        posts = PostPortfolio.objects.all()  # PostPortfolio 모델의 게시물을 가져옵니다.
    elif category == 'postproject':
        posts = PostProject.objects.all()  # PostProject 모델의 게시물을 가져옵니다.
    elif category == 'postquestion':
        posts = PostQuestion.objects.all()  # PostQuestion 모델의 게시물을 가져옵니다.

    # 가져온 게시물을 템플릿에 전달하여 HTML로 렌더링합니다.
    context = {'posts': posts}
    return render(request, 'posts_by_category.html', context)

def post(request):
    return render(request, "post.html")

def post_list(request):
    return render(request, "post_list.html")


class ChatBot():
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.messages = []
        openai.api_key = settings.OPENAI_KEY

    def ask(self, question):
        self.messages.append({
            'role': 'user',
            'content': question
        })
        res = self.__ask__()
        return res

    def __ask__(self):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message['content']
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        return response

    def show_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()


def execute_chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('question')
        chatbot = ChatBot()
        response = chatbot.ask(question)
        return JsonResponse({"response": response})
    return render(request, 'index.html')

def check_duplicate_notification(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        post_id = request.POST.get('post_id')

        # 중복 알림 확인 로직
        duplicate = Notifications.objects.filter(user=recipient_id, post=post_id).exists()

        return JsonResponse({'duplicate': duplicate})
