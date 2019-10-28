from App.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import schedule
import time

def unexpire():
    UserProfile.objects.filter(is_suspended=True).update(is_suspended=False)


def suspend():
    now = datetime.datetime.now() + timezone.timedelta(days=91)
    inactive_users = User.objects.filter(last_login__lt=now)
    for user in inactive_users:
        UserProfile.objects.filter(user=user).update(is_suspended=True)



schedule.every(5).minutes.do(unexpire)
schedule.every(91).days.do(suspend)

while 1:
    schedule.run_pending()
    time.sleep(1)
