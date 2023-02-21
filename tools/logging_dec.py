from django.http import JsonResponse
from django.conf import settings
from user.models import UserProfile
import jwt


def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'code':403, 'error': 'Please login'})
        # 校验jwt
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY)
        except Exception as e:
            print('jwt decode error, {}'.format(e))
            return JsonResponse({'code':403, 'error': 'Please login'})

        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.myuser = user
        return func(request, *args, **kwargs)
    return wrap


def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY)
        except Exception as e:
            return None
    else:
        return None
    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user
