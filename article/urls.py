from .views import base_views,question_views,answer_views
from django.urls import path
app_name = 'article'
urlpatterns = [
    #name -> url에서 article부분을 index로 통칭해서 사용. 만약 앱 명을 바꾸거나 템플릿을 변경하는 경우 url이 바뀌어도 index로 수정없이 사용할 수 있음
    path('', base_views.indexh,name='index'),
    path("insert2/",base_views.insert2),
    path("show2/",base_views.show2),
    path("<int:question_id>/",base_views.detail,name='detail'), #url에 article/정수가 들어오면 detail실행. question_id는 request와 함께 detail에 전달. detail에서는 파라미터로 사용
    path("answer/create/<int:question_id>/",answer_views.answer_create,name="answer_create"),
    path("question/create/",question_views.question_create,name="question_create"),
    path("question/modify/<int:question_id>/",question_views.question_modify,name="question_modify"),
    path("question/delete/<int:question_id>/",question_views.question_delete,name="question_delete"),
    path("answer/modify/<int:answer_id>/",answer_views.answer_modify,name="answer_modify"),
    path("answer/delete/<int:answer_id>/",answer_views.answer_delete,name="answer_delete"),
    path("question/vote/<int:question_id>/",question_views.question_vote,name="question_vote"),
    path("answer/vote/<int:answer_id>/",answer_views.answer_vote,name="answer_vote"),
]