from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    phone = models.IntegerField(null=True)
    joined = models.DateField(null=True, auto_now_add=True)
    age = models.IntegerField(default=0)


class Court(models.Model):
    name = models.CharField(max_length=64)
    ground_type = models.CharField(max_length=32)  # grass, harden, mud, carpet


class Resevation(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
