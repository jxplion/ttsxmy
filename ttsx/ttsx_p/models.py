from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)



class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=50)
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    gclick = models.IntegerField(default=0)
    gunit = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    gst = models.CharField(max_length=200)
    gkc = models.IntegerField(default=100)
    gcontent = HTMLField()
    gtype = models.ForeignKey('TypeInfo')
