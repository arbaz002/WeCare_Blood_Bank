# Generated by Django 3.1.1 on 2020-09-19 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_donor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ongoingdonation',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('In Process', 'In Process')], default='In Process', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='comments',
            field=models.CharField(choices=[('Standard', 'Standard'), ('Urgent', 'Urgent'), ('Critical', 'Critical')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('Fulfilled', 'Fulfilled'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=200, null=True),
        ),
    ]