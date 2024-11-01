from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author_question')#유저 레코드 삭제시 해당 레코드를 외래키로 갖는 Question 레코드 함께 삭제
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null = True,blank = True)#blank =True -> form으로 만들었을 때 is_valid()로 유효성 검사시 값이 비어있어도 통과되도록 하는 코드
    voter = models.ManyToManyField(User,related_name='voter_question') #related_name-> 키를 이용한 User테이블 참조시 N:M 형태로 참조 한다는 의미
                                                                        #

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='author_answer')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null = True,blank = True)
    voter = models.ManyToManyField(User,related_name='voter_answer')

    def __str__(self):
        return self.content[:20]
    
class Test(models.Model):
   name = models.CharField(max_length=200)


class Test2(models.Model):
   name = models.CharField(max_length=200)