from django.shortcuts import render

def main(request):
    return render(request, 'index/main.html')

def index(request):
    return render(request, 'index/index.html')
