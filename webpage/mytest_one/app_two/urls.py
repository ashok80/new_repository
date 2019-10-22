from django.urls import path, re_path

from .views import (DashBoradHome)



urlpatterns = [
    re_path(r'^home/$',DashBoradHome.as_view(), name="dashboard_home"),
]