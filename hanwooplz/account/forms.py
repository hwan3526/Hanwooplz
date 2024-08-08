from django import forms
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='아이디', label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput, label='비밀번호', label_suffix='')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return cleaned_data
            else:
                self.add_error('password', '비밀번호를 확인해주세요')
        except User.DoesNotExist:
            self.add_error('username', '등록된 아이디가 아닙니다')

        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='비밀번호(최소 8자리, [영어 , 숫자, 특수문자] 중 2개 이상 섞어서)',
    )
    password2 = forms.CharField(widget=forms.PasswordInput, label='비밀번호 확인')
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'job', 'tech_stack', 'career', 'career_detail', 'introduction', 'github_link', 'linkedin_link']
        labels = {            
            'username': '유저 아이디',
            'full_name': '이름', 
            'job': '직무', 
            'tech_stack': '주력 기술 스택',
            'career': '경력',
            'career_detail': '경력세부사항',
            'introduction': '한줄 소개',
            'github_link' : 'github 링크',
            'linkedin_link' : 'linkedin 링크',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 등록된 이메일입니다.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 사용중인 아이디 입니다')  
        return username


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'username', 'email', 'full_name', 'job', 'tech_stack', 'career', 'career_detail', 'introduction', 'github_link', 'linkedin_link']
        labels = {
            'profile_image': '프로필 이미지',
            'username': '유저 아이디',
            'full_name': '이름',
            'job': '직무',
            'tech_stack': '주력 기술 스택',
            'career': '경력',
            'career_detail': '경력 세부사항',
            'introduction': '한줄 소개',
            'github_link' : 'GitHub 링크',
            'linkedin_link' : 'LinkedIn 링크',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Set 'github_link' and 'linkedin_link' fields as not required
        self.fields['profile_image'].required = False
        self.fields['github_link'].required = False
        self.fields['linkedin_link'].required = False
        self.fields['username'].help_text = ''
