from django.contrib import admin
from . import models
# from App import models
from App.models import Products
from App.models import Supplier
from App.models import UserProfile, PasswordResetHistory
# from App.models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name_plural = 'User Profile'
    raw_id_fields = ['user']
    fields = ['user', 'location', 'OrgName', 'role', 'failed_login_attempts', 'is_suspended', 'last_suspended']


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    list_select_related = ('userprofile',)

    def get_location(self, instance):
        return instance.userprofile.location

    get_location.short_description = 'location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(Supplier)
admin.site.register(Products)
admin.site.register(UserProfile)
admin.site.register(PasswordResetHistory)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Account)
# admin.site.register(UserProfile)
