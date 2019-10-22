from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    authenticate, get_user_model)
from django.contrib import messages

# Create your views here.

class LoginViewClass(TemplateView):
    template_name = 'app_one/login.html'

    def post(self, request):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('dashboard:dashboard_home'))
        else:
            messages.error(self.request, 'Please Check your username and password')
            return redirect(reverse('account:login'))

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/account/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
