from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#로그인 페이지 만들 때 auth앱을 사용했을 경우, 당연히 회원가입도 해당 앱에 있는 모듈과 연결해서 작업해 줘야 함
class UserForm(UserCreationForm):
    email = forms.EmailField(label='email')
    class Meta:
        model = User
        fields = ("username","password1","password2","email")