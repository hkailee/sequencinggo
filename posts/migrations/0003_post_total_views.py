# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_auto_20160830_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_views',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='views_performed', blank=True),
        ),
    ]
