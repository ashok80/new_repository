from django.apps import AppConfig
from App.tasks import unexpire


class AppConfig(AppConfig):
    name = 'App'
