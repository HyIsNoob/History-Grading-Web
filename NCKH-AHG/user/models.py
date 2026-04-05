from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class CustomerUser(AbstractUser):
    uid = models.AutoField(primary_key=True)
    role_choice = ((0, "Students"), (1, "Teachers"))
    lop = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=30)
    phone_number = models.CharField(default=0, max_length=15)
    subject = models.CharField(max_length=20, default='History') 
    stt = models.IntegerField(default=0)
    role = models.IntegerField(choices=role_choice, default=0)
    avt = models.ImageField(null=True, blank=True)
