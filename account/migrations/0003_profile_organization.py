# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20160902_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='organization',
            field=models.CharField(blank=True, null=True, max_length=256),
        ),
    ]
