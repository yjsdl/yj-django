from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin



class BlockedIPSMiddleware(MiddlewareMixin):
    '''中间件类'''
    EXCLUDE_IPS = ['172.16.179.152']
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''视图函数调用之前会调用'''
        # 获取浏览器端的ip地址
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>Frobidden</h1>')


class TestMiddleware(object):
    """中间件类"""
    def __init__(self):
        '''服务器重启之后，接收第一个请求是调用'''
        print('----init---')

    def process_request(self, request):
        '''产生request对象之后，url匹配之前调用'''
        print('---process_reuqest---')

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''url匹配之后，视图函数调用之前调用'''
        print('---process_view---')

    def process_response(self, request, response):
        '''视图函数调用之后，内容返回浏览器之前'''
        print('---process_response---')
        return response

