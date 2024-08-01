from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout as log_out, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View

from account.forms import LoginForm, CustomUserCreationForm, UserProfileForm
from account.models import UserProfile
from post.models import Post
from portfolio.models import PostPortfolio
from project.models import PostProject
from qna.models import PostQuestion


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
            username = form.get('username')
            password = form.get('password1')
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
            portfolio = PostPortfolio.objects.filter(post=post).first()
            portfolio_list.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'portfolio_id': portfolio.id,
            })
        elif post.category == 1:
            project = PostProject.objects.filter(post=post).first()
            project_list.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'project_id': project.id,
            })
        elif post.category == 2:
            qna = PostQuestion.objects.filter(post=post).first()
            qna_list.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'qna_id': qna.id,
            })

    context = {
        'user_id': user_info.id,
        'username': user_info.username,
        'full_name': user_info.full_name,
        'job': user_info.job,
        'tech_stack': user_info.tech_stack,
        'career': user_info.career,
        'career_detail': user_info.career_detail,
        'introduction': user_info.introduction,
        'github_link': user_info.github_link,
        'linkedin_link': user_info.linkedin_link,
        'user_img': user_info.user_img,
        'portfolio_list': portfolio_list,
        'project_list': project_list,
        'qna_list': qna_list,
    }
    return render(request, 'account/user_info.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user_profile = form.save(commit=False)
            
            if 'user_img' in request.FILES:
                user_img = request.FILES['user_img']
                filename = f'user_img_{user_profile.id}_{user_img.name}'
                user_profile.user_img.save(filename, user_img)
            
            user_profile.save()
            
            return redirect('/@'+form.fields['username'])
    else:
        form = UserProfileForm(instance=request.user)
        form.fields['username'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True

    return render(request, 'account/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, request.user) 
            return redirect(reverse('account:login'))
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'account/change_password.html', {'password_change_form': password_change_form})
