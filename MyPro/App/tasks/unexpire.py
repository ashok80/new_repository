from celery import shared_task
from celery_once import QueueOnce

from App.models import UserProfile


@shared_task(base=QueueOnce, once={'graceful': True})
def unexpire():
    UserProfile.objects.filter(is_suspended=True).update(is_suspended=False)


if __name__ == '__main__':
    unexpire()
