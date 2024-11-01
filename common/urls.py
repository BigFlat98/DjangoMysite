from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'common'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html') , name = 'login'), 
    #auth_views.LoginView.as_view() login기능을 쉽게 구현하기 위한 함수 호출.
    #as_view(~) 이 안에 템플릿 위치를 정해줄 수 있음

    path('logout/', views.logout_views , name = 'logout'), 
    path('signup/', views.signup , name = 'signup'), 
]