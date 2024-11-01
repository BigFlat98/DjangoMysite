from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse ,HttpResponseNotAllowed
from .models import Test2, Question,Answer
from django.utils import timezone
from .forms import QuestionForm,AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required #로그인이 됐는지 안됐는지 확인할 수 있는 메소드. 사용법은 question_create, answer_create에서 확인
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'index.html')

def indexh(request):
    #context -> model과 templete은 서로 직집적인 상호작용이 안됨. model의 데이터는 view에서 참조가 가능하기 때문에 현재 위치인 view에서 model을 import해
    #data를 가져오고(가져오면 json 형태로 전달받고 파이썬에서 변수에 저장하면 dictionary형으로 저장됨) 이제 이 변수에 저장된 값을 template에 있는 html에 보내줄거임.
    #이를 위한 변수
    question_list = Question.objects.order_by('-create_date') #[:10] #날짜가 최신인 것 부터 가져옴. 그래서 -를  붙인것.
                                                                     #+ [:10] -> 가져오는 데이터가 리스트기 때문에 슬라이싱으로 원하는 만큼 가져올 수도 있다.
                                                                     #근데 이런 경우 가져온 데이터가 10개가 안되면 인덱스 에러가 발생
    paginator = Paginator(question_list,10) #Paginator를 이용해 가져온 데이터를 10개씩 나눠서. 모자라면 가져올 수 있는 만큼 가져옴
    page_obj = paginator.get_page(request.GET.get('page','1'))#나눠놓은 페이지 중 몇번째 페이지를 가져올지 정하는 함수.
                                                                #request.GET.get('page','1') -> url뒤에 /?page=1이 들어오면 10개씩 자른 리스트 중 첫번째 출력
                                                                #url뒤에 page에 대한 url을 우리가 적을 필요없이 초기값이 ?page=1로 적용됨.
                                                                #이 코드는 그냥 10개짜리 하나를 계속 보여주는 코드.
    context = {"question_list":page_obj}
    return render(request,'article/question_l.html',context) #import를 하지 않아도 html을 가져올 수 있는건 setting.py의 템플릿 경로(dirs)설정해 줬기 때문임.
                                        #템플릿 설정 안하고 경로 박아도 됨.
                                        #즉.article/question_l.html 이건 -> 앞에 /Users/daejunehwang/dj_vscode/djangoP/mysite/templates 이게 생략 돼있음.
                                        #저 앞에 오는 경로를 setting.py의 템플릿 dirs 설정임
    #question_list = [객체1,객체2,객체3] -> 파이썬에서는 레코드를 객체로 나타내기 때문에 레코드들을 가져오면 각각의 값이 객체 형태로 구현된 리스트가 가져와짐
    

def index(request):
    return HttpResponse("<h1>안녕하세요 NewProject에 오신 것을 환영합니다.</h1><br/>")

def insert2(request):
    for i in range(300):
        q = Question(subject = f"test data : {i}",
                     content = "test",
                     create_date = timezone.now())
        q.save()
    return HttpResponse("데이터 입력 완료")

def show2(request):
    display_all = Test2.objects.all()
    result = ""
    for t in display_all:
        result += "<h1> "+ t.name + "</h1>" + "<br>"
    return HttpResponse(result)

def detail(request,question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id) #pk=primary key, quesion_id가 pk값과 다른게 들어오면 404띄움. 있으면 object가져옴
    context = {"question" : question}
    return render(request,'article/question_detail.html',context)

@login_required(login_url='common:login')#아래 함수가 호출됐을 때 로그인이 안돼있으면 파라미터로 보내는 url호출.
def answer_create(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('article:detail',question_id = question.id)
    else: 
        return HttpResponseNotAllowed('only POST method can use')
    context = {'question':question,'form':form}
    return render(request,'article/question_detail.html',context)

@login_required(login_url='common:login')#아래 함수가 호출됐을 때 로그인이 안돼있으면 파라미터로 보내는 url호출.
def question_create(request) : 
    if request.method == 'POST': #question_form에서 저장하기 버튼을 누르면 post방식으로 이 함수가 다시 호출됨.
        form = QuestionForm(request.POST) #그럼 입력받은 값들을 QuestionForm 객체에 넣고
        if form.is_valid(): #해당 객체가 Form형식이 맞으면(Form유효성 검사. 폼의 자체적인 기능)
            question = form.save(commit=False)  #save()는 QuestionFrom 객체로 저장된 데이터를 Question 객체를 만들어서 거기에 저장.
                                                #save() 함수가 호출되면 위에서 말한 내용대로 Question 객체에 값을 저장 하면서 모듈에 저장까지 하게됨.
                                                #commit이 이 모듈에 값을 저장하는 절차이고 
                                                #아직 create_date가 값이 저장이 안됐기 때문에 commit을 False처리
            question.author = request.user
            question.create_date = timezone.now() #
            question.save() #시간값 저장 했으니까 최종적으로 저장된 값을 모듈에 저장
            return redirect('article:index')#이거 쉽지 않다...
    else: #detail에서 답변등록 버튼을 누를 때는 get방식으로 이 함수가 호출되기 때문에 이 else문 실행.(평소)
        form = QuestionForm()
    return render(request,'article/question_form.html',{'form':form})


@login_required(login_url = 'common:login')
def question_modify(request,question_id) : 
    question = get_object_or_404(Question, pk=question_id)#현재 내가 url을 통해서 호출됐을 때 받아온 question_id를 키로 갖는 레코드 가져옴
    if request.user != question.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect('article:detail',question_id = question.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST,instance=question)#가지고온 레코드로 인스턴스를 만들어서 폼 레코드 생성
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('article:detail',question_id = question.id)
    else:
        form = QuestionForm(instance=question)#기존 정보를 폼 레코드에 넣음
    return render(request,'article/question_form.html',{'form':form}) #헷갈림* 템플릿이 같은거지 url이 같은게 아님. 웹에서 저장하기 누르면 modify url로 다시옴.

@login_required(login_url = 'common:login')
def question_delete(request,question_id) : 
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭세 권한이 없습니다.")
        return redirect('article:detail',question_id = question.id)
    question.delete() #레코드를 테이블에서 삭제
    return redirect('article:index')


def answer_modify(request,answer_id) : 
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect('article:detail',question_id = answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('article:detail',question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request,'article/answer_form.html',{"form":form})

@login_required(login_url = 'common:login')
def answer_delete(request,answer_id) : 
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question
    if request.user != answer.author:
        messages.error(request, "삭세 권한이 없습니다.")
        return redirect('article:detail', question_id=question.id)
    answer.delete() #레코드를 테이블에서 삭제
    return redirect('article:detail', question_id=question.id)
    



