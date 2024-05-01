from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model 
from .models import *

User = get_user_model()


# class RegistrationForm(UserCreationForm):
#     password1 = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
#     password2 = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")
#     email = forms.EmailField()
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'full_name', 'job', 'tech_stack', 'career', 'career_detail', 'introduction']
#         labels = {
#             'username': '유저 아이디',
#             'full_name': '이름', 
#             'job': '직무', 
#             'tech_stack': '주력 기술 스택',
#             'career': '경력',
#             'career_detail': '경력세부사항',
#             'introduction': '한줄 소개'
#         }

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('이미 사용중인 아이디 입니다')  
#         return username
    
#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = ''

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('이미 사용중인 이메일 입니다.')
#         return email

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
#         return password2

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']
