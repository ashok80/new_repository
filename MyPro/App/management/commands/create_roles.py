from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

USER_ROLES = [
    "Employee",
    "Manager"
]


class Command(BaseCommand):
    help = 'Create Initial Groups'

    def handle(self, *args, **options):
        for grp in USER_ROLES:
            Group.objects.create(
                name=grp
            )
            print(grp + ' created...')
