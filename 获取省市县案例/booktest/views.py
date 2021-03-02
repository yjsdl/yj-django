from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from booktest.models import PicTest, AreaInfo

# Create your views here.

# 禁止一些ip地址访问网站(生成一个装饰器)
EXCLUDE_IPS = ['172.16.179.152']
def blocked_ips(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        # 获取浏览器端的ip地址
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in EXCLUDE_IPS:
            return HttpResponse('<h1>Frobidden</h1>')
        else:
            return view_func(request, *view_args, **view_kwargs)
        return wrapper



# /static_test
# @blocked_ips
def static_test(request):
    '''静态文件'''
    return render(request, 'booktest/static_test.html')

# index
# @blocked_ips
def index(request):
   """首页"""
   return render(request, 'booktest/index.html')

# show _upload
def show_upload(request):
    '''显示上传图片页面'''
    return render(request, 'booktest/upload_pic.html')

# upload_handle
def upload_handle(request):
    '''用户上传图片的处理'''
    # 1.获取上传文件的处理对象
    # 上传文件不大于2.5m，文件放在内存中
    # 上传文件大于2.5m，文件内容写到一个临时文件
    pic = request.FILES['pic']
    # 获取上传文件的名字
    # print(pic.name)
    # 2.创建一个文件
    save_path = '%s/booktest/%s'% (settings.MEDIA_ROOT, pic.name)
    with open(save_path, 'wb') as f:
        # 3.获取上传文件的内容并写到创建的文件中
        # pic.chunks分块返回文件的内容，并可以遍历
        for content in pic.chunks():
            f.write(content)
    # 4.在数据库中保存上传记录
    PicTest.objects.create(goods_pic='booktest/%s'% pic.name)
    # 5.返回
    return HttpResponse('ok')

# show_area
# 前段访问的时候，需要传递页码
from django.core.paginator import Paginator
def show_area(request, pindex):
    '''页面分页'''
    # 1.查出所有省级地区的信息
    areas = AreaInfo.objects.filter(aParent__isnull=True)
    # 2.分页，每页显示10条数据
    paginator =  Paginator(areas, 10)
    # print(paginator.num_pages)总页数
    # print(paginator.page_range)页码

    # 3.获取第pindex页的内容
    if pindex == '':
        # 默认获取第一页的内容
        pindex =1
    else:
        pindex = int(pindex)
    # page是page类的实例对象
    page = paginator.page(pindex)
    # 2.使用模板
    return render(request, 'booktest/show_area.html', {'page':page})

def areas(request):
    '''省市县选择案例'''
    return render(request, 'booktest/areas.html')
# prov
def prov(request):
    '''获取所有省级地区的信息'''
    # 1.获取所有省级地区的信息
    areas = AreaInfo.objects.filter(aParent__isnull=True)
    # 2.变量areas并拼接出json数据:atitle id
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))
    # 2.返回数据
    return JsonResponse({'data': areas_list})

# city
def city(request, pid):
    '''获取省下面市级地区的信息'''
    # 获取pid对应地区的下级地区
    # area = AreaInfo.objects.get(id=pid)
    # areas = area.areainfo_set.all()
    areas = AreaInfo.objects.filter(aParent__id = pid)
    # 2.变量areas并拼接出json数据:atitle id
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))
    # 2.返回数据
    return JsonResponse({'data': areas_list})

# dis
def dis(request, pid):
    '''获取市下面县级地区的信息'''
    # 1.获取pid对应地区的下级地区
    areas = AreaInfo.objects.filter(aParent__id = pid)
    # 2.变量areas并拼接出json数据:atitle id
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))
    # 3.返回数据
    return JsonResponse({'data': areas_list})
