from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name='myhome_index'),
    url(r'^login/$', views.login,name='myhome_login'),
    url(r'^logout/$', views.logout,name='myhome_logout'),
    url(r'^register/$', views.register,name='myhome_register'),
    url(r'^list/$', views.list,name='myhome_list'),
    url(r'^info/$', views.info,name='myhome_info'),
    url(r'^vcode/$', views.vcode,name='myhome_vcode'),
]