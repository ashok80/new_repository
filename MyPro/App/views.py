from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import pdb
from django.views.generic import TemplateView, FormView
from .forms import SignUpForm, PasswordResetRequestForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import re
from .models import UserProfile, PasswordResetHistory
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            UserProfile.objects.create(user=user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        # import pdb;
        pdb.set_trace()
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(username = username)
        except:
            errors = [
                'User does not exists....!'
            ]
            res = {
                'errors': errors
            }
            return render(request, 'registration/login.html', res)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            print('sucessss')
            return redirect('home')
        else:
            profile = UserProfile.objects.get(user=user_obj)
            attempts = profile.failure_login_attempts + 1
            if attempts > 10:
                errors = [
                    'Too many number of attempts. Account Blocked Please reset password.....!'
                ]
            else:
                errors = [
                    'Password mismatch',
                    str(attempts)+' / 10 failure attempst of '
                ]
            res = {
                'errors': errors,
                'username': username
            }
            profile.failure_login_attempts = attempts
            profile.save()
            return render(request, 'registration/login.html', res)
         
    else:
        return render(request, 'registration/login.html')

# @login_required
# def my_view(request):
#     if not request.user.is_authenticated:
#         # return render(request,'App/login.html')
#         return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#
#
# class PickyAuthenticationForm(AuthenticationForm):
#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise forms.ValidationError(
#                 ("This account is inactive."),
#                 code='inactive',
#             )
#         if user.username.startswith('t'):
#             raise forms.ValidationError(
#                 ("Sorry, accounts starting with 't' aren't welcome here."),
#                 code='no_b_users',
#             )

# def user_login(request):
    # model = UserProfile

    # def roles(self, instance):
    #     return instance.userprofile.role
    # if roles == "manager":
    #     return redirect(request, 'admin')

    # if request.user.userprofile.role == "manager":
    #     pass
    # if request.user.userprofile.role == "employee":
    #     pass
        # return redirect(request,'login')
        # return redirect(request, '/admin')
        # # return redirect('restricted.html')

    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(username=username,)
    #     user = user.get('user')
    #     role = user.get('role')
    #     if user.role == "manager":
    #         return redirect('home')
    #     if user.role == "employee":
    #         return redirect('admin')


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if date.today() - user.password_date > timedelta(days=90):
                # Redirect to password change page
                return _("Your account has been expired")
            else:
                login(request, user)
                # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            return _("Your account is disabled")
        # else:
        #     # Return an 'invalid login' error message.
        #     return _("Invalid Login")
        if user.is_admin:
            if date.today() - user.password_date > timedelta(days=90):
                return _("Your account has been expired")
            else:
                login(request, user)
        else:
            return _("Your account is disabled")
    else:
        return _("Invalid Login")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


