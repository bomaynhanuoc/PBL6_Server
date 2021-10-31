# Generated by Django 3.1.8 on 2021-10-27 07:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(default='', max_length=30)),
                ('participants', models.TextField(blank=True, default='{}')),
                ('title', models.TextField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('link_contest', models.CharField(blank=True, default='', max_length=100)),
                ('link_datatrain', models.CharField(blank=True, default='', max_length=100)),
                ('link_datatest', models.CharField(blank=True, default='', max_length=100)),
                ('link_tester', models.CharField(blank=True, default='', max_length=100)),
                ('time_regist', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('time_start', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('time_end', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('language', models.TextField(blank=True, default='[]')),
                ('time_out', models.FloatField(blank=True, max_length=100)),
            ],
        ),
    ]
