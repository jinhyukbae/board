from django import forms
from pybo.models import Question,Answer


class QuestionForm(forms.ModelForm): # forms.ModelForm models.py에 question 함수(모델)랑 연결
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성

        labels = {
            'subject':'제목',
            'content':'내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content'] # 답변만 있으면 되므로 subject(제목) 불필요

        labels = {
            'content':'답변내용',
        }