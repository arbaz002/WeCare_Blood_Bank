# Generated by Django 3.1.1 on 2020-09-17 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200917_1533'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BloodBags',
            new_name='BloodBag',
        ),
        migrations.RenameModel(
            old_name='Requests',
            new_name='Request',
        ),
    ]
