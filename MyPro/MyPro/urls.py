"""MyPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^restricted/', TemplateView.as_view(template_name='restricted.html'), name='restricted'),
    # url(r'^password/$', views.change_password, name='change_password'),
    url(r'^password/', views.change_password, name='password'),
    url(r'^confirm-password-hash/', views.confirm_password_hash, name='confirm-password-hash'),
]
