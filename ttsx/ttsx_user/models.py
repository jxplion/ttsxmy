from django.db import models

# Create your models here.


class Userinfo(models.Model):
    user_name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=40)
    user_email = models.CharField(max_length=20)
    user_addr = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=11)
    user_shou = models.CharField(max_length=20)
    user_mailcode = models.CharField(max_length=6)