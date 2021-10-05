from django.db import models
from rest_framework import serializers


class Accounts(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30, default='member')
    token = models.CharField(max_length=100, default='', blank=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['username', 'password', 'role', 'token']
