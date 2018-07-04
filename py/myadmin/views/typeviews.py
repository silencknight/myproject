from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

from .. models import Types,Goods

# 添加分类
@permission_required('myadmin.insert_types',raise_exception=True)
def add(request):
    if request.method == 'GET':
        ob = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path') 
        for i in ob:
            if i.pid==0:
                i.pname='顶级分类'
            else:
                i.pname = Types.objects.get(id=i.pid).typename
                num = i.path.count(',')-1
                i.typename='|---'*num+i.typename
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

# 分类列表
@permission_required('myadmin.show_types',raise_exception=True)
def list(request):
    types=request.GET.get('type',None)
    keywords=request.GET.get('keyword',None)
    if keywords:
        if types == 'all':
            ob = Types.objects.filter(
                Q(id__contains=keywords)|
                Q(typename__contains=keywords)|
                Q(pid__contains=keywords)
                ).extra(select={'path':'concat(path,id)'}).order_by('path') 
        elif types == 'id':
            ob = Types.objects.filter(id__contains=keywords).extra(select={'path':'concat(path,id)'}).order_by('path') 
        elif types == 'typename':
            ob = Types.objects.filter(typename__contains=keywords).extra(select={'path':'concat(path,id)'}).order_by('path') 
        elif types == 'pid':
            ob = Types.objects.filter(pid__contains=keywords).extra(select={'path':'concat(path,id)'}).order_by('path') 
    else:
        ob = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path') 
    for i in ob:
        if i.pid==0:
            i.pname='顶级分类'
        else:
            i.pname = Types.objects.get(id=i.pid).typename
            num = i.path.count(',')-1
            i.typename='|---'*num+i.typename
    paginator = Paginator(ob,10)
    p = request.GET.get('p',1)
    ob = paginator.page(p)
    # print(paginator.num_pages)
    return render(request,'myadmin/type/list.html',{'typelist':ob})

# 修改分类信息
@permission_required('myadmin.edit_types',raise_exception=True)
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

# 删除分类
@permission_required('myadmin.del_types',raise_exception=True)
def delete(request):
    id = request.GET['id']
    # print(id)
    flg = Types.objects.filter(pid=id).exists()
    flg2 = Goods.objects.filter(typeid__id=id).exists()
    # print(flg,flg2)
    if not (flg or flg2):
        ob = Types.objects.get(id=id)
        # ob2 = Types.objects.filter(id__gt=id).first()
        # print(ob2.id)
        ob.delete()
        msg='删除成功'
    else:
        msg='删除失败'
    return JsonResponse({'msg':msg,'del':(flg or flg2)})

