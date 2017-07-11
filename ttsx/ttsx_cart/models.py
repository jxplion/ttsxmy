from django.db import models

# Create your models here.

class CartInfo(models.Model):
    goods = models.ForeignKey('ttsx_p.GoodsInfo')
    user = models.ForeignKey('ttsx_user.Userinfo')
    count = models.IntegerField()