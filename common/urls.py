from django.urls import path
from django.contrib.auth import views as auth_views # 장고 로그인 기능 내장 함수
from . import views

app_name = 'common' # app name을 common 아래 path 파라미터 name을 login이라 했으므로
# navbar.html 로그인 url을 common:login이라 할 수 있다

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

# LoginView가 common 디렉터리의 템플릿을 참조할 수 있도록 template_name='common/login.html'로 설정