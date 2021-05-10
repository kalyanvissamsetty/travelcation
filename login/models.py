
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True) 
    fullname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=32)