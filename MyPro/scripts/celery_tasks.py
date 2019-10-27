from django_celery_beat.models import PeriodicTask, IntervalSchedule
import App

schedule, created = IntervalSchedule.objects.get_or_create(
    every=5,
    period=IntervalSchedule.MINUTES
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Change user status to unexpired',
    task=App.tasks.unexpire_users
)