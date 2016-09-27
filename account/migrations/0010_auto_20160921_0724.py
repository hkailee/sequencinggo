# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20160921_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='users/2016/08/29/16499699-Abstract-word-cloud-for-Infectious-disease-with-related-tags-a_qc5tVfa.jpg', upload_to='users/%Y/%m/%d'),
        ),
    ]
