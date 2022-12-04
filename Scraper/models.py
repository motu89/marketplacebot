from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Fb_credentails(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2500, blank=True, null=True)
    price = models.CharField(max_length=2500, blank=True, null=True)
    location = models.CharField(max_length=2500, blank=True, null=True)
    desc = models.TextField(max_length=25000, blank=True, null=True)
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    tag1 = models.CharField(max_length=2500, blank=True, null=True)
    tag2 = models.CharField(max_length=2500, blank=True, null=True)
    tag3 = models.CharField(max_length=2500, blank=True, null=True)
    tag4 = models.CharField(max_length=2500, blank=True, null=True)
    tag5 = models.CharField(max_length=2500, blank=True, null=True)




