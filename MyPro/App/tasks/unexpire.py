from celery import shared_task
from celery import task
from MyPro.celery import shared_task
from celery import current_task
from celery import Celery
from App.models import UserProfile

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task(bind=True)
def unexpire_task():
    print("Asdfasdfasdf")
    UserProfile.objects.filter(is_suspended=True).update(is_suspended=False)


if __name__ == '__main__':
    unexpire()
