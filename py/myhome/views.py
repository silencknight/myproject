from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse

from myadmin.models import Users,Types,Goods,Address,Orders,OrderInfo,Citys

from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

# 首页
def index(request):
    data = []
    # 获取所有分类，上架商品
    ob = Types.objects.filter(pid = 0)
    for i in ob:
        i.typesub = Types.objects.filter(pid = i.id)
        for j in i.typesub:
            j.goodssub = Goods.objects.filter(typeid=j.id).exclude(status=1)
            data.append(j)
            #  i.typesub.goodssub
    return render(request,'myhome/index.html',{'tlist':ob,'glist':data})

# 登录
def login(request):
    nest = request.GET.get('next','/')
    if request.method == 'GET':
        return render(request,'myhome/login.html')
    elif request.method == 'POST':
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1);</script>')
        try:
            ob = Users.objects.get(username=request.POST['username'])
            # 检测密码
            res = check_password(request.POST['password'],ob.password)
            if res:
                # print(request.session)
                request.session['User']={'uid':ob.id,'username':ob.username}
                return HttpResponse('<script>alert("登陆成功");location.href="'+nest+'"</script>')
        except:
            pass
        return  HttpResponse('<script>alert("用户名或密码错误");history.back(-1);</script>')

# 登出
def logout(request):
    request.session['User']={}
    return HttpResponse('<script>alert("退出登录");location.href="/"</script>')

# 注册
def register(request):
    if request.method =='GET':

        return render(request,'myhome/register.html')
    elif request.method == 'POST':
        # 判断验证码
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
        # 接收数据，删除csrf和验证码
        data = request.POST.copy().dict()
        del data['csrfmiddlewaretoken']
        del data['vcode']
        try:
            data['password'] = make_password(data['password'],None,'pbkdf2_sha256')
            ob = Users.objects.create(**data)
            request.session['User']={'uid':ob.id,'username':ob.username}
            print(request.session['User'])
            return HttpResponse('<script>alert("注册成功");location.href="/"</script>')
        except:
            pass
        return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')

# 列表
def list(request):
    key=request.GET.get('keywords',None)
    if key:
        data = Goods.objects.filter(title__contains=key).exclude(status=1)
    else:
        data = Goods.objects.all().exclude(status=1)
    print(data)
    return render(request,'myhome/list.html',{'glist':data,'key':key})

# 列表-分类查询
def list_id(request,uid):
    data = Goods.objects.filter(typeid=uid).exclude(status=1)
    return render(request,'myhome/list.html',{'glist':data,'key':data[0].typeid.typename})

# 商品详情
def info(request,gid):
    try:
        data = Goods.objects.get(id=gid,status=0)
        data.clicknum+=1
        data.save()
        return render(request,'myhome/info.html',{'ginfo':data})
    except:
        return HttpResponse("<script>history.back(-1)</script>")

# 向购物车添加商品
def addcart(request):
    try:
        count = request.session.get('count',0)
        gid = request.GET['id']
        num = int(request.GET['num'])
        print(gid,num)
        data = request.session.get('cart',{})
        if gid in data.keys():
            data[gid]['num'] += num
        else:
            ob = Goods.objects.get(id=gid)
            data[gid] = {'id':ob.id,'title':ob.title,'num':num,'pic':ob.pic,'price':float(ob.price)}
            request.session['count']=count+1
        request.session['cart'] = data
        return HttpResponse(1)
    except:
        return HttpResponse(0)

# 删除购物车中的商品
def delcart(request):
    try:
        cid = request.GET['cid']
        data = request.session['cart']
        del data[cid]
        request.session['count']-=1
        request.session['cart']=data
        return HttpResponse(1)
    except:
        return HttpResponse(0)

# 购物车页面
def cart(request):
    data = request.session.get('cart',None)
    if data:
        data=request.session['cart'].values()
    return render(request,'myhome/cart.html',{'glist':data})

def clearcart(request):
    request.session['cart'] = {}
    request.session['count'] = 0
    return render(request,'myhome/cart.html')

# 验证码
def vcode(request):
    
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

# 修改购物车
def editcart(request):
    gid = request.GET['gid']
    num = request.GET['gnum']
    data = request.session['cart']
    data[gid]['num'] = int(num)
    request.session['cart'] = data
    return HttpResponse(gid+num)

# 订单检查页面
def ordercheck(request):
    res = eval(request.GET['items'])
    data = {}
    tolprice = 0
    tolnum = 0
    for i in res:
        ob = Goods.objects.get(id=i['gid'])
        i['title'] = ob.title
        i['price'] = float(ob.price)
        i['pic'] = ob.pic
        tolprice += i['price']*i['gnum']
        tolnum += i['gnum']
    data['tolnum'] = tolnum
    data['tolprice'] = round(tolprice,2)
    data['items'] = res
    request.session['order'] = data
    addr = Address.objects.filter(uid=request.session['User']['uid'])
    return render(request,'myhome/ordercheck.html',{'addlist':addr,'data':data})

# 添加地址
def newaddress(request):
    try:
        data = eval(request.GET['data'])
        ob = Address()
        ob.name = data['name']
        ob.phone = data['phone']
        ob.address = ''.join(data['address'])
        ob.detail = data['detail']
        ob.uid = Users.objects.get(id=request.session['User']['uid'])
        ob.save()
        return HttpResponse(1)
    except:
        return HttpResponse(0)

# 修改地址
def editaddr(request):
    if request.method=='GET':
        aid = int(request.GET['aid'])
        uid = request.session['User']['uid']
        ob = Address.objects.filter(uid=uid)
        for i in ob:
            if i.id == aid:
                i.status = 1
            else:
                i.status = 0
            i.save()
    elif request.method == 'POST':
        print(request.POST)
    return HttpResponse(0)

# 删除地址
def deladdr(request):
    aid =request.GET['aid']
    ob = Address.objects.get(id=aid)
    ob.delete()
    return HttpResponse(1)

# 创建订单
def createorder(request):
    aid = request.POST['addrid']
    uid = request.session['User']['uid']
    data = request.session['order']
    cart = request.session['cart']

    ob = Orders()
    ob.uid = Users.objects.get(id=uid)
    ob.addressid = Address.objects.get(id=aid)
    ob.tolprice = data['tolprice']
    ob.tolnum = data['tolnum']
    ob.save()

    for i in data['items']:
        obinfo = OrderInfo()
        obinfo.orderid = ob
        obinfo.gid = Goods.objects.get(id=i['gid'])
        obinfo.num = i['gnum']
        obinfo.save()
        del cart[i['gid']]
        request.session['count']-=1

    request.session['cart'] = cart
    request.session['order'] = ''

    return HttpResponse('<script>location.href="/pay/?orderid='+str(ob.id)+'"</script>')

# 付款成功页面
def pay(request):
    orderid = request.GET['orderid']
    data = Orders.objects.get(id=orderid)
    return render(request,'myhome/pay.html',{'order':data})

# 个人中心
def mycenter(request):
    return render(request,'myhome/center/index.html') 

# 我的订单
def myorders(request):
    data = Orders.objects.filter(uid=request.session['User']['uid']).exclude(status=-1)
    return render(request,'myhome/center/myorders.html',{'orderlist':data}) 

# 删除订单
def delorder(request):
    oid = request.GET['oid']
    data = Orders.objects.get(id = oid)
    print(data.status)
    data.status = -1
    data.save()
    return HttpResponse('删除成功')

# 个人信息
def myinfo(request):
    id = request.session['User']['uid']
    ob = Users.objects.get(id = id)
    return render(request,'myhome/center/info.html',{'user':ob})

# session测试
def set(request):
    request.session['abc'] ='aabbcc'
    request.session['def'] ='ddeeff'
    request.session['ghi'] ={'a':1,'b':2}
    return HttpResponse('session set')

def get(request):
    # request.session.clear()
    print(request.session['abc'])
    return HttpResponse('session get')