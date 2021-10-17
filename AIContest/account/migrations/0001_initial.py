# Generated by Django 3.1.8 on 2021-10-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(default='', max_length=200)),
                ('role', models.CharField(default='member', max_length=30)),
                ('token', models.CharField(blank=True, default='', max_length=100)),
                ('key', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
