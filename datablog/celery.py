from celery import Celery
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datablog.settings')

app = Celery('datablog')
app.conf.update(
    BROKER_URL = 'redis://:@127.0.0.1:6379/1'
)

# 自动去注册应用下加载worker函数
app.autodiscover_tasks(settings.INSTALLED_APPS)