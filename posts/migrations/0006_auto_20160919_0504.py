# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20160905_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='posts_voted', to=settings.AUTH_USER_MODEL),
        ),
    ]
