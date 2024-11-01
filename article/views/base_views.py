from django.shortcuts import render,get_object_or_404
from article.models import Question #절대경로. 루트의 기준이 루트 폴더. models가 다른 폴더에 들어가면 경로를 추가해 줘야함
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q

def indexh(request):
    #context -> model과 templete은 서로 직집적인 상호작용이 안됨. model의 데이터는 view에서 참조가 가능하기 때문에 현재 위치인 view에서 model을 import해
    #data를 가져오고(가져오면 json 형태로 전달받고 파이썬에서 변수에 저장하면 dictionary형으로 저장됨) 이제 이 변수에 저장된 값을 template에 있는 html에 보내줄거임.
    #이를 위한 변수
    # question_list = Question.objects.order_by('-create_date') #[:10] #날짜가 최신인 것 부터 가져옴. 그래서 -를  붙인것.
    #                                                                  #+ [:10] -> 가져오는 데이터가 리스트기 때문에 슬라이싱으로 원하는 만큼 가져올 수도 있다.
    #                                                                  #근데 이런 경우 가져온 데이터가 10개가 안되면 인덱스 에러가 발생
    # paginator = Paginator(question_list,10) #Paginator를 이용해 가져온 데이터를 10개씩 나눠서. 모자라면 가져올 수 있는 만큼 가져옴
    # page_obj = paginator.get_page(request.GET.get('page','1'))#나눠놓은 페이지 중 몇번째 페이지를 가져올지 정하는 함수.
    #                                                             #request.GET.get('page','1') -> url뒤에 /?page=1이 들어오면 10개씩 자른 리스트 중 첫번째 출력
    #                                                             #url뒤에 page에 대한 url을 우리가 적을 필요없이 초기값이 ?page=1로 적용됨.
    #                                                             #이 코드는 그냥 10개짜리 하나를 계속 보여주는 코드.
    # context = {"question_list":page_obj}
    # if kw:
    #     question_list = question_list.filter(Q(subject__incotains=kw)|)
    # return render(request,'article/question_l.html',context) #import를 하지 않아도 html을 가져올 수 있는건 setting.py의 템플릿 경로(dirs)설정해 줬기 때문임.
    #                                     #템플릿 설정 안하고 경로 박아도 됨.
    #                                     #즉.article/question_l.html 이건 -> 앞에 /Users/daejunehwang/dj_vscode/djangoP/mysite/templates 이게 생략 돼있음.
    #                                     #저 앞에 오는 경로를 setting.py의 템플릿 dirs 설정임
    # #question_list = [객체1,객체2,객체3] -> 파이썬에서는 레코드를 객체로 나타내기 때문에 레코드들을 가져오면 각각의 값이 객체 형태로 구현된 리스트가 가져와짐
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 질문 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 작성자 검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자 검색
        ).distinct() #distinct() -> 중복 제거
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'article/question_l.html', context)

def detail(request,question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id) #pk=primary key, quesion_id가 pk값과 다른게 들어오면 404띄움. 있으면 object가져옴
    context = {"question" : question}
    return render(request,'article/question_detail.html',context)

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