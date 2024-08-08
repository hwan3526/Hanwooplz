import os
from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout as log_out, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View

from hanwooplz.settings import BASE_DIR
from account.forms import LoginForm, CustomUserCreationForm, UserProfileForm
from account.models import UserProfile
from post.models import Post
from portfolio.models import Portfolio
from project.models import Project
from qna.models import Question, Answer


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/index')
        else:
            form = LoginForm()
            return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/index')

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                else:
                    return redirect('/index')
            else:
                messages.error(request, '로그인에 실패했습니다. 올바른 아이디와 비밀번호를 입력하세요.')

        return render(request, 'account/login.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        log_out(request)
        return redirect('/login')
    else:
        return redirect('/index')

def register(request):
    if request.user.is_authenticated:
        return redirect('/index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/index')
    else:
        form = CustomUserCreationForm()
        return render(request, 'account/register.html', {'form': form})

def find_id(request):
    if request.user.is_authenticated:
        return redirect('/index')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user = get_user_model().objects.filter(full_name=name, email=email).first()

        if user:
            return render(request, 'account/found_id.html', {'username': user.username})
        else:
            return render(request, 'account/not_found.html')
    else:
        return render(request, 'account/find_id.html')

def find_pw(request):
    if request.user.is_authenticated:
        return redirect('/index')

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        user = get_user_model().objects.filter(email=email, username=username).first()

        if user:
            new_password = get_user_model().objects.make_random_password()

            user.set_password(new_password)
            user.save()

            return render(request, 'account/found_pw.html', {'new_password': new_password})
        else:
            return render(request, 'account/not_found.html')
    else:
        return render(request, 'account/find_pw.html')

def user_info(request, username):
    user_info = UserProfile.objects.filter(username=username).first()
    if not user_info:
        return redirect('/index')
    posts = Post.objects.filter(author=user_info)

    portfolio_list = []
    project_list = []
    qna_list = []

    for post in posts:
        if post.category == 0:
            portfolio = Portfolio.objects.filter(post=post).first()
            portfolio_list.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'portfolio_id': portfolio.id,
            })
        elif post.category == 1:
            project = Project.objects.filter(post=post).first()
            project_list.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'project_id': project.id,
            })
        elif post.category == 2:
            qna = Question.objects.filter(post=post).first()
            qna_list.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'qna_id': qna.id,
            })
        elif post.category == 3:
            qna = Answer.objects.filter(post=post).first()
            qna_list.append({
                'content': post.content,
                'created_at': post.created_at,
                'qna_id': qna.id,
            })

    context = {
        'user_id': user_info.id,
        'username': user_info.username,
        'full_name': user_info.full_name,
        'job': user_info.job,
        'tech_stack': user_info.tech_stack.split(),
        'career': user_info.career,
        'career_detail': user_info.career_detail,
        'introduction': user_info.introduction,
        'github_link': user_info.github_link,
        'linkedin_link': user_info.linkedin_link,
        'profile_image': user_info.profile_image,
        'portfolio_list': portfolio_list,
        'project_list': project_list,
        'qna_list': qna_list,
    }
    return render(request, 'account/user_info.html', context)

@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user_profile = form.save(commit=False)

            if 'profile_image' in request.FILES:
                if user_profile.profile_image:
                    user_profile_old = UserProfile.objects.get(id=request.user.id)
                    os.remove(BASE_DIR / user_profile_old.profile_image.name)
                profile_image = request.FILES['profile_image']
                filename = f'{request.user.username}_{profile_image.name}'
                user_profile.profile_image.save(filename, profile_image)

            user_profile.save()

            return redirect('/@'+request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
        form.fields['username'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True

    return render(request, 'account/edit_profile.html', {'form': form})

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/change_password.html', {'form': form})
