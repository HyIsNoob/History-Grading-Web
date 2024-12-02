import abc
from django.db import models
from django.conf import settings
import re
from django.db.models.deletion import CASCADE
from django.db.models.base import Model
from django.db.models.fields import DateField, SlugField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import templatize 
from user.models import CustomerUser
from django.contrib.auth.models import AbstractUser


# Create your models here.

class exam_exam(models.Model):
    eid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(CustomerUser, on_delete=CASCADE)
    max_point = models.FloatField(default=10)
    title = models.CharField(default='', max_length=300)
    description = models.TextField(max_length=700)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    take = models.IntegerField(default=3)
    time = models.TimeField(default=0)
    code = models.IntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)


class exam_question(models.Model):
    qid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(exam_exam, on_delete=CASCADE)
    max_point = models.FloatField(default=0)
    title = models.CharField(default='', max_length=300)
    description = models.CharField(default='', max_length=500)
    answergv = models.CharField(default='', blank=True, max_length=700)
    cauhoi = models.IntegerField(default=1, blank=False)
    # def __str__(self):
        #return self.eid

class exam_answerkey(models.Model):
    kid = models.AutoField(primary_key=True)
    qid = models.ForeignKey(exam_question, on_delete=CASCADE)
    key = models.TextField(default='')

class exam_primarykey(models.Model):
    pkid = models.AutoField(primary_key=True)
    kid = models.ForeignKey(exam_answerkey, on_delete=CASCADE)
    point = models.FloatField(default=0)
    pkey = models.TextField(default='')


class exam_answer(models.Model):
    aid = models.AutoField(primary_key=True)
    qid = models.ForeignKey(exam_question, on_delete=CASCADE)
    uid = models.ForeignKey(CustomerUser, on_delete=CASCADE)
    answer = models.CharField(default='', max_length=700)
    point = models.FloatField(default=0)
    create = models.DateField(auto_now_add=True)