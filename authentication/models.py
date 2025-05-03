from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Phone No')

    picture = models.ImageField(upload_to='ProfileImages', blank=True, verbose_name='Photo')

    gender = models.CharField(max_length=25, blank=True, null=True, verbose_name='Gender')
    profession = models.CharField(max_length=25, blank=True, null=True)

    otp = models.CharField(max_length=25, blank=True, null=True, verbose_name='OTP')

    last_login_display = models.DateTimeField(default=timezone.now, verbose_name='Last Login Display')

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Updated At')


    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.owner.username