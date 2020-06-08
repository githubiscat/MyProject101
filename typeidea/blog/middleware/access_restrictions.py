from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class AccessRestrictionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        r_path = request.path
        # 对以下地址限制访问频率
        if r_path.startswith(('/post/','/tag/','/category/', '/search/')) or r_path=='/':
            if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
                remote_ip = request.META.get('HTTP_X_FORWARDED_FOR')
            elif request.META.__contains__('REMOTE_ADDR'):
                remote_ip = request.META.get('REMOTE_ADDR')
            else:
                remote_ip = 'Unknow'
            remote_ip_key = str(remote_ip) + 'site_request'
            _ipkey = cache.get(remote_ip_key)
            if _ipkey == None:
                cache.set(remote_ip_key, 1, timeout=6)
            elif _ipkey == 'restrict_access':
                return HttpResponse('<h3>朋友,请不要着急! 小站成本有限,扛不住你频繁刷新! 请{}s后再试...</h3>'.
                                    format(cache.ttl(remote_ip_key)))
            elif _ipkey == 'black':
                return HttpResponse('<h3>你已经被小站列入黑名单,明天自动解封! 小站成本有限,扛不住呀,求高手放过!</h3>')
            elif _ipkey < 5:
                cache.incr(remote_ip_key)
            else:
                cache.set(remote_ip_key, 'restrict_access', timeout=60)
                return HttpResponse('<h3>朋友,请不要着急! 小站成本有限,扛不住你频繁刷新! 请一分钟后再试...</h3>')