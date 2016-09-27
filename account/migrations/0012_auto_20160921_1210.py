# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20160921_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(upload_to='users/%Y/%m/%d', default='users/2016/08/29/test.jpg'),
        ),
    ]
