from django.shortcuts import render
from django.http import HttpResponse
import re

class AdminLoginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self,request):
        # 获取当前用户的请求路径
        u = request.path
        # 定义允许的路径
        urllist = ['/myadmin/login/']
        # 判断是否要进入后台
        if re.match('/myadmin/',u) and u not in urllist:
            # 判断是否登录
            if not request.session.get('_auth_user_id',None):
                # 否则跳转到登录界面
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/"</script>')

        urllist = ['/ordercheck/','/newaddress/','/createorder/','/mycenter/','/myorders/','/pay']
        # 判断是否进入了前台需要登录的界面
        if u in urllist:
            # 检测session中是否存在 adminlogin的数据记录
            if not request.session.get('User',None):
                # 如果在session没有记录,则证明没有登录,跳转到登录页面
                return HttpResponse('<script>alert("请先登录");location.href="/login/?next='+u+'";</script>')

        response = self.get_response(request)
        return response