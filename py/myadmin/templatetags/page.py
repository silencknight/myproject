from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def Page(count,request):
    p = int(request.GET.get('p',1))
    a = p-4

    if a<1: a=1
    if p>count-5: a=count-9
    u=''
    for i in request.GET:
        if i !='p':
            u+='&'+i+'='+request.GET[i]
    s=''
    s+='<li'
    if p==1: s+=' class="am-disabled"'
    s+='><a href="?p=1'+u+'"><<</a></li>'
    if p<=1:
        s+='<li class="am-disabled"><a href="?p=1'+u+'"><</a></li>'
    else:
        s+='<li><a href="?p='+str(p-1)+u+'"><</a></li>'
    for i in range(a,a+10):
        if a>0:
            if i == p:
                s+='<li class="am-active"><a href="?p='+str(i)+u+'">'+str(i)+'</a></li>'
            else:
                s+='<li><a href="?p='+str(i)+u+'">'+str(i)+'</a></li>'
    if p>=count:
        s+='<li class="am-disabled"><a href="?p=1'+u+'">></a></li>'
    else:
        s+='<li><a href="?p='+str(p+1)+u+'">></a></li>'
    s+='<li'
    if p==count: s+=' class="am-disabled"'
    s+='><a href="?p='+str(count)+u+'">>></a></li>'            
    return format_html(s)