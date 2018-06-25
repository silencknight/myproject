from django.shortcuts import render
from django.http import HttpResponse
from . userviews import uploads
from .. models import Goods,Types

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
            return HttpResponse('<script>alert("添加成功");location.href="'+reserve('myadmin_goods_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reserve('myadmin_goods_add')+'"</script>')

def list(request):
    ob = Goods.objects.all()
    return render(request,'myadmin/goods/list.html',{'goodslist':ob})

def edit(request):

    return HttpResponse('edit')

def delete(request):

    return HttpResponse('delete')
