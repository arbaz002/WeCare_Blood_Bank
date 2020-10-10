# Generated by Django 3.1.1 on 2020-09-17 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('hid', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('hname', models.CharField(max_length=200, null=True)),
                ('haddress', models.CharField(max_length=200, null=True)),
                ('hphone', models.CharField(max_length=200, null=True)),
                ('hemail', models.EmailField(max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='donor',
            name='dgender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('rid', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('bloodgroup', models.CharField(max_length=10, null=True)),
                ('amount', models.IntegerField()),
                ('comments', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(choices=[('Fulfilled', 'Fulfilled'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], max_length=200, null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='OngoingDonation',
            fields=[
                ('bid', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('bloodgroup', models.CharField(max_length=10, null=True)),
                ('quantity', models.IntegerField()),
                ('donatedate', models.DateField()),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=200, null=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.donor')),
            ],
        ),
        migrations.CreateModel(
            name='BloodBags',
            fields=[
                ('bbid', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('bloodgroup', models.CharField(max_length=10, null=True)),
                ('quantity', models.IntegerField()),
                ('donatedate', models.DateField()),
                ('expirydate', models.DateField()),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.donor')),
            ],
        ),
    ]