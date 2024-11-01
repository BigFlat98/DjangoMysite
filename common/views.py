from django.shortcuts import render, redirect
from django.contrib.auth import logout,authenticate,login
from common.forms import UserForm
# Create your views here.


def logout_views(request):
    logout(request)
    return redirect('index')

def signup(request):#request에는 html에 있는 head,body의 데이터들이 딕셔너리 형태로 쭉 나열돼있음.
    if request.method == 'POST':
        form = UserForm(request.POST) #request 딕셔너리에 있는 POST키의 value들. 즉 내가 form에 입력된 값들이 리턴됨 
        if form.is_valid():#유효성 검사, 필요한 값이 다 들어왔냐
            form.save()#입력받은 값을 테이블에 저장
            
            #회원가입하면 가입한 값으로 바로 로그인 되도록 설정
            username = form.cleaned_data.get('username') #테이블에 저장된 username값을 변수에 저장. 값을 안전하게 가져올 수 있도록 하는 클래스 cleaned_data
            raw_password = form.cleaned_data.get('password1')#테이블에 저장된 password값을 변수에 저장
            user = authenticate(username = username, password = raw_password) #사용자 인증. 테이블에 있는 값이랑 파라미터 값을 비교,검사.
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html',{'form':form})
    
