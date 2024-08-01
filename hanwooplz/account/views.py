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
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email, username=username)
        except user_model.DoesNotExist:
            # 사용자를 찾을 수 없음
            return render(request, 'account/not_found.html')

        # 새로운 임시 비밀번호 생성
        new_password = user_model.objects.make_random_password()

        # 비밀번호 업데이트
        user.set_password(new_password)
        user.save()

        # 사용자에게 새로운 비밀번호 전달하는 방법 (이메일 등)

        # 여기에서는 임시 비밀번호를 템플릿을 통해 보여줍니다.
        context = {
            'new_password': new_password,
        }
        return render(request, 'account/found_pw.html', context)
    else:
        return render(request, 'account/find_pw.html')

def found_pw(request):
    # Your code to render the password reset done page goes here
    return render(request, 'account/found_pw.html')

def myinfo(request, user_id):
    userinfo = UserProfile.objects.get(id=user_id)
    user_posts = Post.objects.filter(author=userinfo)

    selected_category = request.GET.get('category', 'postportfolio')

    posts = []

    for post in user_posts:
        if selected_category == 'postportfolio':
            category = 'portfolio'
            postcategory = PostPortfolio.objects.filter(post=post).first()
        elif selected_category == 'postproject':
            category = 'project'
            postcategory = PostProject.objects.filter(post=post).first()
        elif selected_category == 'postquestion':
            category = 'question'
            postcategory = PostQuestion.objects.filter(post=post).first()

        if postcategory:
            posts.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'post_id': postcategory.id,
                'category': category,
            })

    context = {
        'user_id': userinfo.id,
        'username': userinfo.username,
        'full_name': userinfo.full_name,
        'job': userinfo.job,
        'tech_stack': userinfo.tech_stack,
        'career': userinfo.career,
        'career_detail': userinfo.career_detail,
        'introduction': userinfo.introduction,
        'posts': posts,
        'github_link': userinfo.github_link,
        'linkedin_link': userinfo.linkedin_link,
        'selected_category': selected_category,
        'user': userinfo,
    }
    return render(request, 'account/myinfo.html', context)

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
