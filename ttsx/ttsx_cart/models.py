from django.db import models

# Create your models here.

class CartInfo(models.Model):
    goods = models.ForeignKey('ttsx_p.GoodsInfo')
    user = models.ForeignKey('ttsx_user.Userinfo')
    count = models.IntegerField()


class OrderMain(models.Model):
    orderid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('ttsx_user.Userinfo')
    orderdate = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    status = models.IntegerField(default=0)


class OrderDetial(models.Model):
    order = models.ForeignKey(OrderMain)
    goods = models.ForeignKey('ttsx_p.GoodsInfo')
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
