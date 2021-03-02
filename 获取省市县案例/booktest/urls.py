from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^static_test', views.static_test),# 静态文件
    url(r'^index$', views.index), # 首页
    url(r'^show_upload$', views.show_upload), # 显示上传图片页面
    url(r'^upload_handle$', views.upload_handle),# 用户上传图片的处理
    url(r'^show_area(?P<pindex>\d*)$', views.show_area), # 页面分页
    url(r'^areas$', views.areas),# 省市县选择案例
    url(r'^prov$', views.prov), # 获取所有省级地区的信息
    url(r'^city(\d+)$', views.city), # 获取省下面市级地区的信息
    # url(r'^dis(\d+)$', views.dis), # 获取市下面县级地区的信息
    url(r'^dis(\d+)$', views.city), # 获取市下面县级地区的信息
]
