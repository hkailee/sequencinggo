# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('user_from', models.ForeignKey(related_name='rel_from_set', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(related_name='rel_to_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d')),
                ('role', models.CharField(choices=[('scientist', 'Scientist'), ('bioinformatician', 'Bioinformatician'), ('clinician', 'Clinician')], max_length=10, default='scientist')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
