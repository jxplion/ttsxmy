# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_p', '0002_initial'),
        ('ttsx_user', '0002_auto_20170707_1725'),
        ('ttsx_cart', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('goods', models.ForeignKey(to='ttsx_p.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMain',
            fields=[
                ('orderid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('orderdate', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('status', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='ttsx_user.Userinfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetial',
            name='order',
            field=models.ForeignKey(to='ttsx_cart.OrderMain'),
        ),
    ]
