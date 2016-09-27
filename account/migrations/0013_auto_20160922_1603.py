# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20160921_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='users/2016/09/19/default_profile.png', upload_to='users/%Y/%m/%d'),
        ),
    ]
