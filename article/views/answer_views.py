from django.shortcuts import render,get_object_or_404,redirect,resolve_url #resolve_url
from django.http import HttpResponseNotAllowed
from ..models import Question,Answer
from django.utils import timezone
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required #로그인이 됐는지 안됐는지 확인할 수 있는 메소드. 사용법은 question_create, answer_create에서 확인
from django.contrib import messages

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
            return redirect('{}#answer_{}'.format(resolve_url('article:detail',question_id = question.id),answer.id))
            #'{}#answer_{}'.format(resolve_url('article:detail',question_id = question.id),answer.id)
            #-> {'article:detail',question_id = question.id}#answer_{'article:detail',question_id = question.id}
            #-> 원래 보내려는 url을 호출 하는데 뒤에 생성한 answer의 id를 엘리멘트 id로 갖는 위치로 이동.
    else: 
        return HttpResponseNotAllowed('only POST method can use')
    context = {'question':question,'form':form}
    return render(request,'article/question_detail.html',context)

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
            return redirect('{}#answer_{}'.format(resolve_url('article:detail',question_id = answer.question.id),answer.id))
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

def answer_vote(request,answer_id):
    answer = get_object_or_404(Answer,pk=answer_id)
    if request.user == answer.author:
        messages.error(request,"자추 금지")
        return redirect('article:detail',question_id = answer.question.id)
    else:
        answer.voter.add(request.user)
        return redirect('{}#answer_{}'.format(resolve_url('article:detail',question_id = answer.question.id),answer.id))
    