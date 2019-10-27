from django.contrib.auth.models import User
from App.models import UserProfile
from django.utils import timezone
from datetime import datetime


def expire_inactive_users():
    timeframe = datetime.today() - timezone.timedelta(days=91)
    users = User.objects.filter(last_login__lt=timeframe)
    for user in users:
        UserProfile.objects.get(user=user).update(is_suspended=True)


if __name__ == '__main__':
    expire_inactive_users()
