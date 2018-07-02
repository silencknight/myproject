from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from .. models import Orders,OrderInfo,Users

# Create your views here.

def list(request):
    data = Orders.objects.all()
    for i in data:
        i.sub = OrderInfo.objects.filter(orderid__id=i.id)
    paginator = Paginator(data,10)
    p = request.GET.get('p',1)
    data = paginator.page(p)
    return render(request,'myadmin/order/list.html',{'olist':data})

def edit(request):
    oid = request.GET['oid']
    if request.method == 'GET':
        ob = Orders.objects.get(id=oid)
        return render(request,'myadmin/order/edit.html',{'order':ob})
    elif request.method == 'POST':
        try:
            ob = Orders.objects.get(id=oid)
            data = request.POST.copy().dict()
            ob.status = data['status']
            ob.uid = Users.objects.get(username=data['username'])
            ob.tolprice = data['tolprice']
            ob.tolnum = data['tolnum']
            # print(ob.status, ob.uid, ob.tolprice, ob.tolnum)
            ob.save()
            return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_order_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_order_edit')+'?oid='+str(oid)+'"</script>')