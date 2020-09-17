from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import auth

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = CreateAccount(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('input')
    else:
        form = CreateAccount()

    return render(request, 'sign_up.html', {'form': form})


# 로그인
def login(request):
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = User.objects.get(username=username, password=password)

        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, 'login.html')


# 로그 아웃
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')