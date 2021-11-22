# Generated by Django 3.2.9 on 2021-11-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DriverState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_id', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('state', models.CharField(choices=[('Idle', 'idle'), ('Engaged', 'engaged'), ('Offline', 'offline')], default='offline', max_length=7)),
            ],
        ),
    ]
