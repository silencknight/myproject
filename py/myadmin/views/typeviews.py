from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse

from .. models import Types

def add(request):
    if request.method == 'GET':
        ob = Types.objects.all()
        return render(request,'myadmin/type/add.html',{'typelist':ob})
    elif request.method == 'POST':
        try:
            ob = Types()
            ob.typename = request.POST['typename']
            ob.pid = request.POST['pid']
            ob.path = ''
            if ob.pid != '0':
                ob.path+= Types.objects.get(id=ob.pid).path
            ob.path+=ob.pid+','
            ob.save()
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse("myadmin_type_list")+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse("myadmin_type_add")+'?typename='+request.POST['typename']+'"</script>')

def list(request):
    ob = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path')
    for i in ob:
        if i.pid==0:
            i.pname='顶级分类'
        else:
            i.pname = Types.objects.get(id=i.pid).typename
            num = i.path.count(',')-1
            i.pname='|---'*num+i.typename
    return render(request,'myadmin/type/list.html',{'typelist':ob})

def edit(request):
    ob = Types.objects.get(id=request.GET['tid'])
    if request.method=='GET':
        return render(request,'myadmin/type/edit.html',{'tinfo':ob})
    elif request.method=='POST':
        try:
            ob.typename = request.POST['typename']
            ob.save()
            return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_type_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_type_edit')+'?tid='+str(request.GET['tid'])+'"</script>')

def delete(request):
    id = request.GET['id']
    print(id)
    return JsonResponse({'delete':1})
