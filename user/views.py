import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from user.models import UserProfile
from django.utils.decorators import method_decorator
from tools.logging_dec import logging_check
from django.core.cache import cache
from tools.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms_c
import random


import hashlib
#异常码 10100 - 10199


# Create your views here.
#FBV
@logging_check
def users_views(request, username):

    if request.method != 'POST':
        result = {'code':10103, 'error': 'Please use POST'}

    user = request.myuser

    avatar = request.FILES['avatar']
    user.avatar = avatar
    user.save()
    return JsonResponse({'code': 200})


#更灵活[可继承]
#对未定义的http method请求 直接返回405响应
class UserViews(View):

    def get(self,request, username=None):
        #/v1/users
        #/v1/users/chuchu
        if username is None:
            # /v1/users
            ...
        else:
            # /v1/users/chuchu
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                result = {'code':10102, 'error':'The username is wrong'}
                return JsonResponse(result)
            result = {'code':200, 'username': username, 'data':{
                'info':user.info, 'sign': user.sign, 'nickname':user.nickname, 'avatar':str(user.avatar)
            }}
            return JsonResponse(result)
        return JsonResponse({'code':200,'msg':'test'})

    def post(self, request):

        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        sms_num = json_obj['sms_num']

        #参数基本检查
        if password_1 != password_2:
            result = {'code': 10100, 'error': 'The password is not same'}
            return JsonResponse(result)

        # 比对验证码是否正确
        old_code = cache.get('sms_{}'.format(phone))
        if not old_code:
            result = {'code': '10110', 'error': 'The code is wrong'}
            return JsonResponse(result)
        if int(sms_num) !=  old_code:
            result = {'code': '10110', 'error': 'The code is wrong'}
            return JsonResponse(result)

        #检查用户名是否可用
        old_users = UserProfile.objects.filter(username=username)
        if old_users:
            result = {'code':10101, 'error': 'The username is already existed'}
            return JsonResponse(result)

        #UserProfile插入数据(密码md5存储)
        p_m = hashlib.md5()
        p_m.update(password_1.encode())  # 字符转成字节
        # p_m.hexdigest() 16进制存储
        UserProfile.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email, phone=phone)

        result = {'code':200, 'username':username, 'data':{}}
        return JsonResponse(result)

    @method_decorator(logging_check)
    def put(self, request, username=None):
        json_str = request.body
        json_obj = json.loads(json_str)

        user = request.myuser
        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']

        user.save()
        return JsonResponse({'code': 200})


def sms_view(request):
    if request.method != 'POST':
        return JsonResponse({'code':10108, 'error':'Please use POST'})

    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']

    print(phone)
    # 生成随机码
    code = random.randint(1000, 9999)
    # 储存随机码 django-redis
    cache_key = 'sms_{}'.format(phone)
    old_code = cache.get(cache_key)
    if old_code:
        return JsonResponse({'code':10111, 'error':'The code is already existed'})

    cache.set(cache_key, code, 180)
    # res = send_sms(phone, code)
    # print('phone', phone, 'code', code)
    # if res.get('statusCode') != '000000':
    #     return JsonResponse({'code': 10109, 'error': 'code send fail'})

    send_sms_c.delay(phone, code)
    # 发送随机码
    return JsonResponse({'code':200})


def send_sms(phone, code):
    config = settings.YUNCONFIG
    yun = YunTongXin(**config)
    res = yun.run(phone, code)
    return res

















