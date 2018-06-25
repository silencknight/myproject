from django.conf.urls import url
from . views import views,userviews,typeviews,goodsviews

urlpatterns = [
    url(r'^$', views.index,name='myadmin_index'),
    url(r'^user/add/$', userviews.add,name='myadmin_user_add'),
    url(r'^user/list/$', userviews.list,name='myadmin_user_list'),
    url(r'^user/edit/$', userviews.edit,name='myadmin_user_edit'),
    url(r'^user/delete/$', userviews.delete,name='myadmin_user_delete'),

    url(r'^type/add/$', typeviews.add,name='myadmin_type_add'),
    url(r'^type/list/$', typeviews.list,name='myadmin_type_list'),
    url(r'^type/edit/$', typeviews.edit,name='myadmin_type_edit'),
    url(r'^type/delete/$', typeviews.delete,name='myadmin_type_delete'),

    url(r'^goods/add/$', goodsviews.add,name='myadmin_goods_add'),
    url(r'^goods/list/$', goodsviews.list,name='myadmin_goods_list'),
    url(r'^goods/edit/$', goodsviews.edit,name='myadmin_goods_edit'),
    url(r'^goods/delete/$', goodsviews.delete,name='myadmin_goods_delete'),
]