# Generated by Django 3.1.1 on 2020-09-18 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_hospital_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='user',
        ),
    ]