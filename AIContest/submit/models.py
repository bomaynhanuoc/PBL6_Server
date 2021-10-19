from django.db import models
from rest_framework import serializers
from datetime import datetime


class Submits(models.Model):
    id_contest = models.IntegerField(default=0)
    username = models.CharField(max_length=30, default='')
    language = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=30, default='Pending')
    time_submit = models.DateTimeField(default=datetime.now, blank=True)
    link_submit = models.CharField(max_length=100, default='')


class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submits
        fields = '__all__'
