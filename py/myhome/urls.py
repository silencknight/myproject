from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name='myhome_index'),
    url(r'^login/$', views.login,name='myhome_login'),
    url(r'^logout/$', views.logout,name='myhome_logout'),
    url(r'^register/$', views.register,name='myhome_register'),
    url(r'^list/$', views.list,name='myhome_list'),
    url(r'^list/([0-9]+)/$', views.list_id,name='myhome_list_id'),
    url(r'^info/([0-9]+)/$', views.info,name='myhome_info'),
    url(r'^vcode/$', views.vcode,name='myhome_vcode'),
    url(r'^addcart/$', views.addcart,name='myhome_addcart'),
    url(r'^delcart/$', views.delcart,name='myhome_delcart'),
    url(r'^cart/$', views.cart,name='myhome_cart'),
    url(r'^ordercheck/$', views.ordercheck,name='myhome_ordercheck'),
    url(r'^editcart/$', views.editcart,name='myhome_editcart'),
    url(r'^editaddr/$', views.editaddr,name='myhome_editaddr'),
    url(r'^deladdr/$', views.deladdr,name='myhome_deladdr'),
    url(r'^newaddress/$', views.newaddress,name='myhome_newaddress'),
    url(r'^createorder/$', views.createorder,name='myhome_createorder'),
    url(r'^mycenter/$', views.mycenter,name='myhome_mycenter'),
    url(r'^myorders/$', views.myorders,name='myhome_myorders'),
    url(r'^delorder/$', views.delorder,name='myhome_delorder'),
    url(r'^myinfo/$', views.myinfo,name='myhome_myinfo'),
    url(r'^pay/$', views.pay,name='myhome_pay'),
    url(r'^sesset/$', views.set,name='myhome_set'),
    url(r'^sesget/$', views.get,name='myhome_get'),
]