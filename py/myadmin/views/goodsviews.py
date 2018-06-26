from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from . userviews import uploads
from .. models import Goods,Types
import os

# Create your views here.

def add(request):
    if request.method=='GET':
        ob = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path')
        for i in ob:
            if i.pid==0:
                pass
            else:
                i.pname = Types.objects.get(id=i.pid).typename
                num = i.path.count(',')-1
                i.pname='|---'*num+i.typename
        return render(request,'myadmin/goods/add.html',{'typelist':ob})
    elif request.method=='POST':
        try:
            ob = request.POST.copy().dict()
            pic = request.FILES.get('pic',None)
            pic = uploads(request)
            del ob['csrfmiddlewaretoken']
            ob['pic']=pic
            ob['typeid']= Types.objects.get(id=ob['typeid'])
            print(ob)
            Goods.objects.create(**ob)
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_goods_add')+'"</script>')

def list(request):
    ob = Goods.objects.all()
    return render(request,'myadmin/goods/list.html',{'goodslist':ob})

def edit(request):
    id = request.GET['gid']
    gb = Goods.objects.get(id=id)
    if request.method=='GET':
        ob = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path')
        for i in ob:
            if i.pid==0:
                pass
            else:
                i.pname = Types.objects.get(id=i.pid).typename
                num = i.path.count(',')-1
                i.pname='|---'*num+i.typename
        return render(request,'myadmin/goods/edit.html',{'typelist':ob,'goodslist':gb})
    elif request.method=='POST':
        try:
            gb.title = request.POST['title']    
            gb.descr = request.POST['descr']
            gb.price = request.POST['price']
            gb.store = request.POST['store']
            gb.info = request.POST['info']
            gb.typeid = Types.objects.get(id=request.POST['typeid'])
            if request.FILES.get('pic',None):
                os.remove('.'+gb.pic)
                gb.pic=uploads(request)
            gb.save()
            return HttpResponse('<script>alert("修改成功");location.href="'+reverse("myadmin_goods_list")+'"</script>')
        except:
            return HttpResponse('<script>alert("修改失败");location.href="'+reverse("myadmin_goods_edit")+'?gid='+str(gb.id)+'&tid='+request.GET['tid']+'"</script>')

def delete(request):
    try:
        id = request.GET.get('id',None)
        ob = Goods.objects.get(id=id)
        if ob.pic:
            os.remove('.'+ob.pic)
        ob.delete()
        return JsonResponse({'msg':'删除成功','del':1})
    except:
        return JsonResponse({'msg':'删除失败','del':0})

