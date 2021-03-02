from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, RequestContext
# Create your views here.

# 登录判断装饰器
def login_required(view_func):
    """登录判断装饰器"""
    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录，调用对应的视图
         return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录，跳转到登录页
            return redirect('/login')
    return wrapper




def my_render(request, template_path, context_dict={}):
    # 1.加载模板文件，获取一个模板对象
    temp = loader.get_template(template_path)
    # 2.定义模板上下文，给模板文件传数据
    context =  context_dict
    # 3.模板渲染，产生一个替换后的html内容
    res_html = temp.render(context)
    # 4.返回应答
    return HttpResponse(res_html)


# /index
def index(request):
    # return my_render(request, 'booktest/index.html')
    return render(request, 'booktest/index.html')


def login(request):
    """显示登录页面"""
    # 判断用户是否登录
    if request.session.has_key('islogin'):
        # 用户已经登录，跳转到修改密码页面
        return redirect('/change_pwd')
    else:
        # 用户未登录
        # 判断用户是否保存在cookie中
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    """登录校视图"""
    # request.POST 保存的是post方式提交的参数
    # request。GET 保存的是get方式提交的参数
    # 1.获取提交的用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')


    # 获取用户输入的验证码
    vcode1 = request.POST.get('vcode')
    # 获取session中保存的验证码
    vcode2 = request.session.get('verifycode')
    # 进行验证码校验
    if vcode1 != vcode2:
        # 验证码错误
        return redirect('/login')

    # 2.进行登录的校验
    if username == 'smart' and password == '123':
        # 用户名密码正确，跳转到修改密码页面
        response = redirect('/change_pwd')
        # 判断是否需要记住用户名
        if remember == 'on':
            # 设置cookie username过期时间为一周
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
        # 记住用户登录状态
        # 只要session中有islogin 就认为用户已经登录
        request.session['islogin'] = True
        # 记住登录的用户名
        request.session['username'] = username
        return response
    else:
        return redirect('/login')


# change_pd
@login_required
def change_pwd(request):
    """显示修改密码页面"""
    # 进行用户是否登录的判断
    # if not request.session.has_key('islogin'):
    #     # 用户未登录，跳转到登录页
    #     return redirect('/login')
    return render(request, 'booktest/change_pwd.html')

# change_pwd_action
@login_required
def change_pwd_action(request):
    """模拟修改密码处理"""
    # 进行用户是否登录的判断
    # if not request.session.has_key('islogin'):
    #     # 用户未登录，跳转到登录页
    #     return redirect('/login')
    # 1.获取新密码
    pwd = request.POST.get('pwd')
    # 获取用户名
    username = request.session.get('username')
    # 2.实际开发的时候，修改对应数据库中的内容...
    # 3.返回一个应答
    return HttpResponse('%s修改密码为：%s' %(username, pwd))


# verify_code
def verify_code(request):
    """登录验证码"""
    pass

# url_reverse
def url_reverse(request):
    '''url反向解析页面'''
    return render(request, 'booktest/url_reverse.html')