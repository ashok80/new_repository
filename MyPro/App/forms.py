from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(
        label="password", min_length=8, max_length=14, required=True, help_text="required field.",
    )

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            raise forms.ValidationError(
                "This password must contain at least 8 characters."
            )
        if not re.findall('\d', password):
            raise forms.ValidationError(
                "The password must contain at least 1 digit, 0-9."
            )
        if not re.findall('[A-Z]', password):
            raise forms.ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z"
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                ("The password must contain at least 1 lowercase letter, a-z."),
                code="password_no_lower",
            )
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise forms.ValidationError(
                "The password must contain at least 1 symbol: " + \
                "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
            )
        return password

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Enter Your Email', required=True, max_length=500)


class ConfirmNewPassword(forms.Form):
    password = forms.CharField(
        min_length=8, max_length=14, required=True, help_text="required field.",
        widget=forms.PasswordInput(attrs={'class': 'form-group'})
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError(
                "This password must contain at least 8 characters."
            )
        if not re.findall('\d', password):
            raise forms.ValidationError(
                "The password must contain at least 1 digit, 0-9."
            )
        if not re.findall('[A-Z]', password):
            raise forms.ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z"
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                ("The password must contain at least 1 lowercase letter, a-z."),
                code="password_no_lower",
            )
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise forms.ValidationError(
                "The password must contain at least 1 symbol: " + \
                "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
            )
        return password

    class Meta:
        model = User
        fields = '__all__'
