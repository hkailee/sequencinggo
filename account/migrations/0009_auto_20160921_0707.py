# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20160921_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(default='scientist', max_length=20, choices=[('scientist', 'Scientist'), ('bioinformatician', 'Bioinformatician'), ('clinician', 'Clinician'), ('justlovecontribute', 'JustLoveContributing')]),
        ),
    ]
