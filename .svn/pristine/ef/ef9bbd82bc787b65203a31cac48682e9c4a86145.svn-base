# coding=utf-8
from django.utils.deprecation import MiddlewareMixin


class addUserNameMiddleWare(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        print('this is __init__')

    def process_request(self, request):
        """生成请求对象后，路由匹配之前"""
        print('this is process_request')

    def process_view(self, request, func, args, kwargs):
        """路由匹配后，视图函数调用之前"""
        print("this is process_view")

    def process_exception(self, request, exception):
        """视图函数发生异常时"""
        print('this is process_exception')

    def process_template_response(self, request, response):
        """'''模板渲染时执行'''"""
        # username = request.session['usermame']
        # response.data['usermame'] = username
        print('this is process_template_response')
        return response

    def process_response(self, request, response):
        """视图函数执行后，响应内容返回浏览器之前"""
        print('this is process_response')
        return response