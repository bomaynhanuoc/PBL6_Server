from django.db import models
from rest_framework import serializers


class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30, default='member')
    token = models.CharField(max_length=100, default='', blank=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'role', 'token']
