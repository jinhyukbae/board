import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()



# 페이징 기능
# 장고에는 더하기 필터 |add:+3는 있는데 빼기 필터는 없음
# |add:-3로 원하는 값을 뺀 결과를 보여줄 수 있으나 add 필터에는 변수를 적용 할 수 없기 때문에 새로 빼기 필터를 정의함
@register.filter # 애너테이션  템플릿에서 해당 함수를 필터로 사용
def sub(value, arg):
    return value - arg # 기존 값 value에서 입력으로 받은 값 arg를 빼서 리턴하는 함수

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"] # nl2br은 줄바꿈 문자를 <br>로 바꿈  fenced_code 마크다운 소스코드 표현을 위해 필요 ##내용 ### 내용 etc..
    return mark_safe(markdown.markdown(value, extensions=extensions))