# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(max_length=10, default='published'),
        ),
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 8, 30, 18, 18, 51, 939968, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
