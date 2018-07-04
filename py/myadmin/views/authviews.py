from django.shortcuts import render,reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from .. models import Users
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.decorators import permission_required


# 后台用户添加
@permission_required('add_user',raise_exception=True)
def useradd(request):
    if request.method == "GET":
        glist = Group.objects.all()
        return render(request,'myadmin/auth/user/add.html',{'glist':glist})
    elif request.method == 'POST':
        if request.POST['is_superuser'] == '1':
            usr = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])
        else: 
            usr = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password']) 
        gs = request.POST.getlist('gs',None)
        usr.groups.set(gs)
        usr.save()
        return HttpResponse('<script>location.href="'+reverse('auth_user_list')+'"</script>')

# 后台用户列表
@permission_required('add_user',raise_exception=True)
def userlist(request):
    data = User.objects.all()
    paginator = Paginator(data,10)
    p = request.GET.get('p',1)
    data = paginator.page(p)
    return render(request,'myadmin/auth/user/list.html',{'userlist':data})

# 后台用户信息修改
@permission_required('add_user',raise_exception=True)
def useredit(request):
    user = User.objects.get(id=request.GET['id'])
    if request.method == 'GET':
        group = Group.objects.filter(user=user)
        ugroup = Group.objects.all().exclude(user=user)
        return render(request,'myadmin/auth/user/edit.html',{'user':user,'group':group,'ugroup':ugroup})
    elif request.method == 'POST':
        try:
            user.username = request.POST['username']
            user.email = request.POST['email']
            # if request.user.username == user.username:
            #     print(1)
            user.is_superuser = request.POST['is_superuser']
            gs = request.POST.getlist('gs',None)
            user.groups.set(gs)
            user.save()
            return HttpResponse('<script>location.href="'+reverse('auth_user_list')+'"</script>')
        except:
            return HttpResponse('<script>location.href="'+reverse('auth_user_edit')+'?id='+str(user.id)+'"</script>')

# 后台用户删除
@permission_required('add_user',raise_exception=True)
def userdelete(request):
    id = request.GET['id']
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponse('<script>location.href="'+reverse('auth_user_list')+'"</script>')

# 权限组添加
@permission_required('add_user',raise_exception=True)
def groupadd(request):
    if request.method == 'GET':
        perms = Permission.objects.all().exclude(name__istartswith='Can')
        return render(request,'myadmin/auth/group/add.html',{'perms':perms})
    elif request.method == 'POST':
        g = Group(name=request.POST['name'])
        g.save()

        prms = request.POST.getlist('prms',None)
        print(prms)
        if prms:
            g.permissions.set(prms)
            g.save()
        return HttpResponse('<script>location.href="'+reverse('auth_group_list')+'"</script>')

# 权限组列表
@permission_required('add_user',raise_exception=True)
def grouplist(request):
    data = Group.objects.all().exclude(name__istartswith='Can')
    for i in data:
        i.count=len(i.user_set.all())
    paginator = Paginator(data,10)
    p = request.GET.get('p',1)
    data = paginator.page(p)
    return render(request,'myadmin/auth/group/list.html',{'group':data})

# 权限组修改
@permission_required('add_user',raise_exception=True)
def groupedit(request):
    gid = request.GET['id']
    data = Group.objects.get(id=gid)
    if request.method == 'GET':
        perms = Permission.objects.exclude(group=data).exclude(name__istartswith='Can')
        return render(request,'myadmin/auth/group/edit.html',{'group':data,'perms':perms})
    elif request.method == 'POST':
        data.name = request.POST['name']
        data.permissions.clear()
        prms = request.POST.getlist('prms',None)
        print(prms)
        if prms:
            data.permissions.set(prms)
        data.save()
        return HttpResponse('<script>location.href="'+reverse('auth_group_list')+'"</script>')

# 后台登录
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

# 后台登出
def mylogout(request):
    logout(request)
    return HttpResponse('<script>alert("退出登录");location.href="/myadmin/login/"</script>')