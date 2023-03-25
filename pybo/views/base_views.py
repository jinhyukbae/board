from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
import logging
logger = logging.getLogger('pybo')

# 같은 디렉토리 안에 있으면 from .models import Question
# views 디렉터리 하위에 위치하므로 ..models
from ..models import Question


def index(request):
    logger.info("INFO 레벨로 출력")
    page = request.GET.get('page',1) # 페이지
    # http://localhost:8000/pybo/?page=1 처럼 get 방식으로 호출 된 url에서 page 값을 가져올 때 사용
    # 페이지값이 없이 호출 되면 자동으로 /1로 설정
    kw = request.GET.get('kw', '') # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색 subject__icontains=kw kw 문자열이 포함되어 있느냐
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색 / 답변을 작성한 사람의 이름에 포함되느냐
        ).distinct()
    #     subject__contains=kw 대신 subject__icontains=kw을 사용하면 대소문자를 가리지 않고 찾아 준다.
    paginator = Paginator(question_list, 10) # 페이지당 10개씩
    # 게시물 전체를 의미하는 question_list 두번 째 파라미터는 페이지당 보여줄 수
    page_obj = paginator.get_page(page)
    #  paginator를 이용하여 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성 이렇게 하면 장고 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경된다
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    #  # question_list는 페이징 객체(page_obj)
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id): # http://localhost:8000/pybo/2/ 페이지가 요청되면  question_id에 2가 세팅
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

