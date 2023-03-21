
from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('',base_views.index, name='index'), # /페이지 요청에 대해 path('', views.index, name='index')가 작동하여 pybo/views.py 파일의 index 함수가 실행

]

