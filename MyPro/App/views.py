from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView
from .forms import SignUpForm, PasswordResetRequestForm, ConfirmNewPassword
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import re
from .models import UserProfile, PasswordResetHistory
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login
from django.utils import timezone
from django.utils.crypto import get_random_string


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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user_obj)
        except Exception as e:
            errors = [
                'User does not exists'
            ]
            res = {
                'errors': errors
            }
            return render(request, 'registration/login.html', res)

        pwd_valid = check_password(password, user_obj.password)

        if pwd_valid and not user_profile.is_suspended:
            login(request, user_obj)
            return redirect('home')
        else:
            if user_profile.failed_login_attempts < 10 and not user_profile.is_suspended:
                user_profile.failed_login_attempts += 1
                user_profile.save()
                attempts = user_profile.failed_login_attempts
                errors = [
                    '{} failed login attempt'.format(attempts)
                ]
                res = {
                    "errors": errors
                }
                return render(request, 'registration/login.html', res)
            else:
                if user_profile.is_suspended:
                    errors = [
                        'Your account has been temporarly suspended due to too many failed login attempts.'
                    ]
                    res = {
                        'errors': errors
                    }
                    return render(request, 'registration/login.html', res)
                else:
                    user_profile.failed_login_attempts = 0
                    user_profile.is_suspended = True
                    user_profile.last_suspended = timezone.now()
                    user_profile.save()
                    errors = [
                        'Your account has been temporarly suspended due to too many failed login attempts.'
                    ]
                    res = {
                        'errors': errors
                    }
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
        email = request.POST.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except Exception as e:
            errors = [
                'User with {} email was not found'.format(email)
            ]
            res = {
                'errors': errors
            }
            return render(request, template_name='accounts/change_password.html', context=res)
        hash = get_random_string(length=32)
        user_profile, created = UserProfile.objects.get_or_create(user=user_obj)
        user_profile.forgot_password_hash = hash
        user_profile.save()

        errors = [
            'An email with the recovery hash has been sent to this email {}'.format(email)
        ]
        res = {
            'errors': errors
        }
        return render(request, template_name='accounts/change_password.html', context=res)

    else:
        return render(request, 'accounts/change_password.html', {})


def confirm_password_hash(request):
    # REQUIRED URL PARAMS email and hash
    if request.method == "GET":
        hash = request.GET.get("hash")
        email = request.GET.get("email")

        if hash and email:
            try:
                user_obj = User.objects.get(email=email)
            except Exception as e:
                errors = [
                    'There was something wrong with the hash you sent please try again.'.format(email)
                ]
                res = {
                    'errors': errors
                }
                return render(request, 'accounts/confirm_password_hash.html', context=res)
            user_profile = UserProfile.objects.get(user=user_obj)
            if user_profile.forgot_password_hash == hash:
                form = ConfirmNewPassword()
                return render(request, 'accounts/confirm_password_hash.html',
                              context={'form': form, 'user': user_obj.email})
            else:
                errors = [
                    'There was something wrong with the hash you sent please try again.'.format(email)
                ]
                res = {
                    'errors': errors
                }
                return render(request, 'accounts/confirm_password_hash.html', context=res)
        else:
            errors = [
                'There was something wrong with the hash you sent please try again.'.format(email)
            ]
            res = {
                'errors': errors
            }
            return render(request, 'accounts/confirm_password_hash.html', context=res)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        form = ConfirmNewPassword(request.POST)

        user_obj = User.objects.get(email=email)
        previous_passwords, created = PasswordResetHistory.objects.get_or_create(user=user_obj)

        if form.is_valid():
            hashed_password = make_password(password)
            print(hashed_password)
            password_history = [previous_passwords.last_user_password, previous_passwords.second_last_user_password, previous_passwords.third_last_user_password,
                                previous_passwords.fourth_last_user_password, previous_passwords.fifth_last_user_password]
            for password in password_history:
                if hashed_password == password:
                    errors = [
                        'You cannot use any of your previous password as the current password.'
                    ]
                    res = {
                        'errors': errors
                    }
                    return render(request, 'accounts/confirm_password_hash.html', context=res)
                else:
                    user_obj.password = hashed_password
                    user_obj.save()

                    errors = [
                        'Your password has been successfully changed.'
                    ]
                    res = {
                        'errors': errors
                    }
                    return render(request, 'accounts/confirm_password_hash.html', context=res)
        else:
            form = ConfirmNewPassword()
            errors = [
                'You cannot use any of your previous password as the current password.'
            ]
            res = {
                'errors': errors,
                'form': form,
                'user': email
            }
            return render(request, 'accounts/confirm_password_hash.html', context=res)
