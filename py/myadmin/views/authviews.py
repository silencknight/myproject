from django.shortcuts import render,reverse
from django.http import HttpResponse
from .. models import Users
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User,Permission,Group


def useradd(request):
    

def mylogin(request):
    if request.method == 'GET':
        return render(request,'myadmin/login.html')

    elif request.method == 'POST':
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");location.href="/myadmin/login/"</script>')

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return HttpResponse('<script>location.href="/myadmin/"</script>')

        return HttpResponse('<script>alert("用户名或密码错误");location.href="/myadmin/login/"</script>')


def mylogout(request):
    logout(request)
    return HttpResponse('<script>alert("退出登录");location.href="/myadmin/login/"</script>')