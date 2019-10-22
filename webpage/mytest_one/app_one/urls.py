from django.urls import path, re_path

from .views import (LoginViewClass, LogoutView)



urlpatterns = [
    path('login/', LoginViewClass.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]