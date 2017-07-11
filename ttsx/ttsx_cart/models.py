from django.db import models

# Create your models here.

class CartInfo(models.Model):
    goods_id = models.ForeignKey('ttsx_p.GoodsInfo')
    user_id = models.ForeignKey('ttsx_user.Userinfo')
    goods_num = models.IntegerField(max_length=1000)