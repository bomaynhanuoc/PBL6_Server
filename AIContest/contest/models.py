from django.db import models
from rest_framework import serializers
from datetime import datetime
from AIContest.AIContest import settings


class Contests(models.Model):
    creator = models.CharField(max_length=30, default='')
    participants = models.TextField(default='{}', blank=True)
    title = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    linkcontest = models.CharField(max_length=100, default='', blank=True)
    linkdatatrain = models.CharField(max_length=100, default='', blank=True)
    linkdatatest = models.CharField(max_length=100, default='', blank=True)
    linktester = models.CharField(max_length=100, default='', blank=True)
    timeregist = models.DateTimeField(default=datetime.now, blank=True, null=True)
    timestart = models.DateTimeField(default=datetime.now, blank=True)
    timeend = models.DateTimeField(default=datetime.now, blank=True)
    language = models.TextField(default='[]', blank=True)


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contests
        fields = '__all__'


