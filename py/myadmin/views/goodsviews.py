from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

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
            # print(ob)
            Goods.objects.create(**ob)
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_goods_add')+'"</script>')

def list(request):
    types = request.GET.get('type',None)
    keywords = request.GET.get('keyword',None)
    if keywords:
        if types == 'all':
            if keywords == '上架':
                status = 0
            else:
                status = 1
            ob = Goods.objects.filter(
                Q(title__contains=keywords)|
                Q(id__contains=keywords)|
                Q(typeid__typename__contains=keywords)|
                Q(status__contains=status)
                ).order_by('typeid')
        elif types == 'id':
            ob = Goods.objects.filter(id__contains=keywords).order_by('typeid')
        elif types == 'title':
            ob = Goods.objects.filter(title__contains=keywords).order_by('title')
        elif types == 'status':
            if keywords == '上架':
                status = 0
            else:
                status = 1
            ob = Goods.objects.filter(status__contains=keywords).order_by('status')
        elif types == 'typeid':
            ob = Goods.objects.filter(typeid__typename__contains=keywords).order_by('typeid')
    else:        
        ob = Goods.objects.all().order_by('typeid')
    paginator = Paginator(ob,10)
    p = request.GET.get('p',1)
    ob = paginator.page(p)
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
        # print(id)
        ob = Goods.objects.get(id=id)
        ob.status = (ob.status+1)%2
        # print(ob.status)
        ob.save()
        return JsonResponse({'del':ob.status})
    except:
        return JsonResponse({'del':ob.status})

