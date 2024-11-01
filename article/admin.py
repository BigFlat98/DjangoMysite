from django.contrib import admin
from .models import Question ,Answer,Test2

# Register your models here.

class QuestionAdmin(admin.ModelAdmin): #admin 테이블 관리 페이지에 subject속성으로 검색하는 검색창 생성
    search_fields = ['subject']

class AnswerAdmin(admin.ModelAdmin): 
    search_fields = ['question']

class Test2Admin(admin.ModelAdmin): 
    search_fields = ['name']


    

admin.site.register(Question, QuestionAdmin) #어드민 창에 각 앱 관리 사이트 생성, 파라미터에 검색창 생성하는 클래스를 추가해야 검색창이 나옴
admin.site.register(Answer) #이러면 그냥 셀렉트 박스가 기본으로 나옴
admin.site.register(Test2,Test2Admin) 
