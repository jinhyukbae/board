from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST": # POST 요청인 경우
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1') # 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            # 인증시 사용할 사용자명과 비밀번호를 얻기 위해 사용
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인 신규 사용자를 생성한 후에 자동 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


# django.contrib.auth.authenticate - 사용자 인증을 담당한다. (사용자명과 비밀번호가 정확한지 검증한다.)
# django.contrib.auth.login - 로그인을 담당한다. (사용자 세션을 생성한다.)