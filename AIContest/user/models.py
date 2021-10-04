from django.db import models
from rest_framework import serializers


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30, default='member')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password', 'role')
