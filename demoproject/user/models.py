from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Register(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30, default='member')