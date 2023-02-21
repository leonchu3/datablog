from datablog.celery import app
from tools.sms import YunTongXin
from django.conf import settings


@app.task()
def send_sms_c(phone, code):
    config = settings.YUNCONFIG
    yun = YunTongXin(**config)
    res = yun.run(phone, code)
    return res

