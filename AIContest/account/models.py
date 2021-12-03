from django.db import models
from rest_framework import serializers


class Accounts(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200, default='')
    role = models.CharField(max_length=30, default='member')
    token = models.CharField(max_length=100, default='', blank=True)
    key = models.CharField(max_length=100, default='')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'
