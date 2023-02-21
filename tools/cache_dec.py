from .logging_dec import get_user_by_request
from django.core.cache import cache


def cache_set(expire):
    def _cache_set(func):
        def wrapper(request, *args, **kwargs):
            # 区分场景-只做列表页
            if 't_id' in request.GET:
                return func(request, *args, **kwargs)
            # 生成出正确的cache key[访客访问和博主访问]
            visitor_user = get_user_by_request(request)
            visitor_username = None
            if visitor_user:
                visitor_username = visitor_user.username
            author_username = kwargs['author_id']
            print('visitor is {}'.format(visitor_username))
            print('author is {}'.format(author_username))
            full_path = request.get_full_path()
            if visitor_username == author_username:
                cache_key = 'topics_cache_self_{}'.format(full_path)
            else:
                cache_key = 'topics_cache_{}'.format(full_path)
            print('cache_key is {}'.format(cache_key))
            # 判断是否有缓存有缓存则直接返回
            res = cache.get(cache_key)
            print('res is {}'.format(res))
            if res:
                print('---cache in')
                return res
            # 执行视图
            res = func(request, *args, **kwargs)
            # 存储缓存 cache对象 / set / get
            cache.set(cache_key, res, expire)
            # 返回响应
            return func(request, *args, **kwargs )
        return wrapper
    return _cache_set