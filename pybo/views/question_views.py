from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# 개져오는 곳보다 더 하위디렉터리에 있으므로 ..
from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면
            question = form.save(commit=False) # 임시 저장하여 question 객체를 리턴받는다.
            question.author = request.user
            question.create_date = timezone.now() # 실제 저장을 위해 작성일시를 설정한다.
            question.save() # 데이터를 실제로 저장한다.
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>와 같이 링크를 통해 페이지를 요청할 경우에는 무조건 GET 방식이 사용되어 else 구문을 타게 되고
# 질문을 등록하는 화면을 렌더링 하게 된다.

# 문 등록 화면에서 subject, content 항목에 값을 기입하고 "저장하기" 버튼을 누르면 이번에는 /pybo/question/create/ 페이지를 POST 방식으로 요청한다.
#  form 태그에 action 속성이 지정되지 않으면 현재 페이지가 디폴트 action으로 설정되기 때문

# GET 방식에서는 form = QuestionForm() 처럼 QuestionForm을 인수 없이 생성했지만 POST 방식에서는 form = QuestionForm(request.POST) 처럼 request.POST를 인수로 생성했다.
# request.POST를 인수로 QuestionForm을 생성할 경우에는 request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성된다.
    # request.POST에는 화면에서 사용자가 입력한 내용들이 담겨있다.
#  form에 저장된 subject, content의 값이 올바르지 않다면 오류메세지와 함께 else 구문을 타고 다시 질문 등록 화면을 렌더링

# . QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 question = form.save(commit=False) 사용 가능
# commit=False는 임시저장  실제 데이터는 아직 데이터베이스에 저장되지 않은 상태
    # form.save(commit=False) 대신 form.save()를 수행하면 Question 모델의 create_date에 값이 없다는 오류가 발생
    # QuestionForm에는 현재 subject, content 속성만 정의되어 있고 create_date 속성은 없기 때문
# 이러한 이유로 임시 저장을 하여 question 객체를 리턴받고 create_date에 값을 설정한 후 question.save()로 실제 데이터를 저장하는 것

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 로그인한 사용자 != 질문의 글쓴이
        messages.error(request, '수정권한이 없습니다') # messages 모듈을 이용한 넌필드 오류 발생
        return redirect('pybo:detail',question_id=question_id)
    if request.method == "POST": # 저장하기 버튼 클릭
        form = QuestionForm(request.POST, instance=question) # 수정된 내용을 반영해야 하는 폼 생성 instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        # 질문 수정화면에서 제목 또는 내용을 변경하여 POST 요청하면 변경된 내용이 QuestionForm에 저장
        if form.is_valid(): #  입력 데이터 검증
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail',question_id=question_id)
    else: # 수정하기 버튼 클릭 http://localhost:8000/pybo/question/modify/2/ 페이지가 GET 방식으로 호출
        form = QuestionForm(instance=question) #GET 요청인 경우 질문수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록 다음과 같이 폼을 생성
        # instance 값을 지정하면 폼의 속성 값이 instance의 값으로 채워짐 질문을 수정하는 화면에서 제목과 내용이 채워진 채로 보임
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천 할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question_id)