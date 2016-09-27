# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique_for_date='created')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('tags', taggit.managers.TaggableManager(verbose_name='Tags', to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.')),
                ('user', models.ForeignKey(related_name='posts_created', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='posts_liked')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comments_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='users_like',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='comments_liked'),
        ),
    ]
