# Generated by Django 3.1.1 on 2020-09-23 19:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200923_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='reqdate',
            field=models.DateField(default=datetime.date(2020, 9, 24)),
        ),
        migrations.AlterField(
            model_name='donationhistory',
            name='donatedate',
            field=models.DateField(default=datetime.date(2020, 9, 24)),
        ),
        migrations.AlterField(
            model_name='donationhistory',
            name='expirydate',
            field=models.DateField(default=datetime.date(2020, 11, 5)),
        ),
        migrations.AlterField(
            model_name='donor',
            name='dob',
            field=models.DateField(default=datetime.date(2020, 9, 24)),
        ),
    ]
