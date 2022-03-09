from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


# 自定义拦截器
class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.method)
        print(request.path)

        if request.path != '/login/' and request.path != '/':
            if request.session.get('user', None):
                pass
            else:
                return HttpResponseRedirect('/')
