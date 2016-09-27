# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160921_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(default='scientist', choices=[('scientist', 'Scientist'), ('bioinformatician', 'Bioinformatician'), ('clinician', 'Clinician'), ('justlovecontribute', 'Just Love contribute')], max_length=20),
        ),
    ]
