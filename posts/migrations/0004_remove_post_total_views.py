# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_total_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='total_views',
        ),
    ]
