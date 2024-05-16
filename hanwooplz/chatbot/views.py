import json

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import openai


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
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('question')
        chatbot = ChatBot()
        response = chatbot.ask(question)
        return JsonResponse({'response': response})
    return render(request, 'index/index.html')
