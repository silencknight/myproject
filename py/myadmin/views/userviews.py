from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .. models import Users
import os

# Create your views here.

def add(request):
    if request.method=='GET':
        return render(request,'myadmin/user/add.html')
    elif request.method=='POST':
        try:
            # print(request/.POST)
            data = request.POST.copy().dict()
            del data['csrfmiddlewaretoken']
            from django.contrib.auth.hashers import make_password,check_password
            data['password']=make_password(data['password'],None)
            if request.FILES.get('pic',None):
                data['pic']=uploads(request)
                if data['pic']==0:
                    return HttpResponse('<script>alert("上传的文件类型不符合要求");location.href="'+reverse('myadmin_user_add')+'"</script>')
            print(data)
            ob = Users.objects.create(**data)
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_user_add')+'"</script>')

def list(request):
    types = request.GET.get('type',None)
    keywords = request.GET.get('keyword',None)
    # print(types,keywords)
    if types:
        if types == 'all':
            data=Users.objects.filter(
                Q(username__contains=keywords)|
                Q(email__contains=keywords)|
                Q(phone__contains=keywords)|
                Q(age__contains=keywords)|
                Q(sex__contains=keywords)
                )
        elif types == 'username':
            data=Users.objects.filter(username__contains=keywords)
        elif types == 'email':
            data=Users.objects.filter(email__contains=keywords)
        elif types == 'phone':
            data=Users.objects.filter(phone__contains=keywords)
        elif types == 'age':
            data=Users.objects.filter(age__contains=keywords)
        elif types == 'sex':
            data=Users.objects.filter(sex__contains=keywords)
    else:
        data=Users.objects.all()
    paginator = Paginator(data,10)
    p = request.GET.get('p',1)
    data = paginator.page(p)
    return render(request,'myadmin/user/list.html',{'userlist':data})

def edit(request):
    id=request.GET.get('uid',None)
    data=Users.objects.get(id=id)
    if request.method == 'GET':
        return render(request,'myadmin/user/edit.html',{'uinfo':data})
    elif request.method == 'POST':
        try:
            data.username=request.POST['username']
            data.email=request.POST['email']
            data.age=request.POST['age']
            data.sex=request.POST['sex']
            data.phone=request.POST['phone']
            if request.FILES.get('pic',None):
                if data.pic:
                    os.remove('.'+data.pic)
                data.pic=uploads(request)
            data.save()
            return HttpResponse('<script>alert("修改成功");location.href="'+reverse("myadmin_user_list")+'"</script>')
        except:
            return HttpResponse('<script>alert("修改失败");location.href="'+reverse("myadmin_user_edit")+'?uid='+str(data.id)+'"</script>')

def delete(request):
    try:
        id = request.GET.get('uid',None)
        # print(id)
        ob = Users.objects.get(id=id)
        # print(ob)
        if ob.pic:
            os.remove('.'+ob.pic)
        ob.delete()
        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}

    return JsonResponse(data)


def uploads(request):
    m = request.FILES.get('pic',None)
    p = m.name.split('.').pop()
    arr = ['jpg','png','jpeg','gif']
    if p not in arr:
        return 0

    import time,random
    filename = str(time.time())+str(random.randint(1,99999))+'.'+p

    d = open("./static/pic/"+filename,"wb+")

    for chunk in m.chunks():
        d.write(chunk)

    d.close()

    return "/static/pic/"+filename
