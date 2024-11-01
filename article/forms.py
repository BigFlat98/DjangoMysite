#페이지에서 form 태그에 데이터를 넣어 url을 보냈을 때 값을 객체 형태로 저장.
#이 값을 views에서 값을 받을 때 편리 및 값이 정상적으로 들어왔는지 검사하기 위해 한번 저장을 거치는 방식
#views에서 이 함수 객체를 가져와서 데이터를 받음
from django import forms
from .models import Question,Answer

class QuestionForm(forms.ModelForm): #폼의 형식에는 일반 form과 modelform이 있음
    class Meta:#ModleForm에 있는 이너 클래스를 재정의해서 사용. modelform 사용을 위한 필수 이너 클래스 재정의
        model = Question #사용할 모델
        fields = ["subject",
                  "content"]
        widgets = {
            'subject' : forms.TextInput(attrs={'class':'form-control'}),#html에서 이 폼 객체를 적어주면 자동으로 html작성을 장고가 해주는데 
                                                                        #그 html class명을 form-control로 설정
            'content' : forms.Textarea(attrs={'class':'form-control','rows':10})
        }
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content' : '답변'
        }