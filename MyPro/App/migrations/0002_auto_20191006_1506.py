# Generated by Django 2.1.12 on 2019-10-06 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.TimeField(auto_now=True)),
                ('password', models.CharField(max_length=500)),
                ('user', models.OneToOneField(on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='failure_login_attempts',
            field=models.IntegerField(default=0, verbose_name='Failure Attempts'),
        ),
    ]
