# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_p', '0002_initial'),
        ('ttsx_user', '0002_auto_20170707_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='ttsx_p.GoodsInfo')),
                ('user', models.ForeignKey(to='ttsx_user.Userinfo')),
            ],
        ),
    ]
