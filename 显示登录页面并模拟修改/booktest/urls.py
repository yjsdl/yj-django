from django.conf.urls import url

from booktest import views

urlpatterns = [
    url(r'^index2', views.index, name='index'), # 主页
    url(r'^login$', views.login),# 登录
    url(r'^login_check$', views.login_check),# 登录校验
    url(r'^change_pwd$', views.change_pwd),# 修改密码
    url(r'^change_pwd_action', views.change_pwd_action),# 模拟修改密码页面
    url(r'^verify_code$', views.verify_code),# 登录验证码
    url(r'^url_reverse$', views.url_reverse),# url反向解析页面
]
