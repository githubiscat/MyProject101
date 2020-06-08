from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class CommentFilterMiddleware(MiddlewareMixin):
    """限制非法用户提交大量垃圾评论"""
    def process_request(self, request):
        req_path = request.path
        if req_path == reverse('reply') or req_path == reverse('comment'):
            if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
                remote_ip = request.META.get('HTTP_X_FORWARDED_FOR')
            elif request.META.__contains__('REMOTE_ADDR'):
                remote_ip = request.META.get('REMOTE_ADDR')
            else:
                remote_ip = 'Unknow'
            _ipkey = cache.get(str(remote_ip))
            if _ipkey == None:
                timeout = 24 * 60 * 60
                cache.set(str(remote_ip), 1, timeout=timeout)
            elif _ipkey == 'lock':
                return HttpResponse('默认每个用户24小时内可以发表30条评论! 小站维护成本低, 请理解!  ')
            elif _ipkey < 100:
                cache.incr(str(remote_ip))
            else:
                t_o = cache.ttl(str(remote_ip))  #查看剩余过期时间
                cache.set(str(remote_ip),'lock', timeout=t_o)

        return