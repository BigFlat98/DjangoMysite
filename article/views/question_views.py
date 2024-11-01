from django.shortcuts import render,get_object_or_404,redirect
from ..models import Question
from django.utils import timezone
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required #로그인이 됐는지 안됐는지 확인할 수 있는 메소드. 사용법은 question_create, answer_create에서 확인
from django.contrib import messages

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

@login_required(login_url = 'common:login')
def question_vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.user == question.author:
        messages.error(request,"자추 금지")
    else:
        question.voter.add(request.user)
    return redirect('article:detail',question_id = question.id)
