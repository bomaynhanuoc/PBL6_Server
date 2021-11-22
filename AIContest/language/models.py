from django.db import models
from rest_framework import serializers


class Languages(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, default='')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'


