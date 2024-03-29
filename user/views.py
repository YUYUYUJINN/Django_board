from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # settings.py의 INSTALLED_APPS에 이미 추가되어 있음
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import login as auth_logout

# Create your views here.
def signup(request):
    if request.method == "GET":
        signupForm = UserCreationForm()  # 장고에서 이미 폼을 만들어둠, import만 해서 사용 가능
        return render(request, 'user/signup.html', {'signupForm': signupForm})
    elif request.method == "POST":
        signupForm = UserCreationForm(request.POST)
        #검증
        if signupForm.is_valid():
            user = signupForm.save(commit=False)
            user.save()

        return redirect('/board/list')


def login(request):
    if request.method == "GET":
        loginForm = AuthenticationForm()
        context = {'loginForm': loginForm}
        return render(request, 'user/login.html', context)
    elif request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            auth_login(request, loginForm.get_user())  # 세션 방식, 토큰 방색 2개가 있음, 여기서는 세션 방식
            return redirect('/board/list')
            # username = request.POST.get('username')
            # password = request.POST.get('password')
            # user = User.objects.get(instance=username)
            # if user.password == password:
            #   로그인 성공
            # else :
            #   로그인 실패

def logout(request):
    auth_logout(request)
    return redirect('/board/listGet')

