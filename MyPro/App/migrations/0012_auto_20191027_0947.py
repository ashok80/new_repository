# Generated by Django 2.1.12 on 2019-10-27 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_auto_20191027_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previouspassword',
            name='fifth_password',
        ),
        migrations.RemoveField(
            model_name='previouspassword',
            name='first_password',
        ),
        migrations.RemoveField(
            model_name='previouspassword',
            name='fourth_password',
        ),
        migrations.RemoveField(
            model_name='previouspassword',
            name='second_password',
        ),
        migrations.RemoveField(
            model_name='previouspassword',
            name='third_password',
        ),
    ]
