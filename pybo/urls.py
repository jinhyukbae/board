from django.urls import path

from .views import base_views, question_views, answer_views

app_name = 'pybo'

urlpatterns = [
    path('', base_views.index, name='index'),  #config/urls.py에 include('pybo.urls')로 default값 설정 되어있으므로 앞을 ''로 둔다.
    path('<int:question_id>/', base_views.detail, name='detail'), # http://localhost:8000/pybo/<int:question_id>/
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'), # {% url 'pybo:answer_vote' answer.id  %}
]