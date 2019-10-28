import os
from celery import Celery
from celery import shared_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyPro.settings')
app = Celery('Mypro')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

