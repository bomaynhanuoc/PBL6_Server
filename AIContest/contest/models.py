from django.db import models
from rest_framework import serializers
from datetime import datetime
from AIContest.AIContest import settings


class Contests(models.Model):
    creator = models.CharField(max_length=30, default='')
    participants = models.TextField(default='{}', blank=True)
    title = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    link_contest = models.CharField(max_length=100, default='', blank=True)
    link_datatrain = models.CharField(max_length=100, default='', blank=True)
    link_datatest = models.CharField(max_length=100, default='', blank=True)
    link_tester = models.CharField(max_length=100, default='', blank=True)
    time_regist = models.DateTimeField(default=datetime.now, blank=True, null=True)
    time_start = models.DateTimeField(default=datetime.now, blank=True)
    time_end = models.DateTimeField(default=datetime.now, blank=True)
    language = models.TextField(default='[]', blank=True)
    time_out = models.FloatField(max_length=100, blank=True)

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contests
        fields = '__all__'


