# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-17 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_topic', '0003_topic_reindex_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='is_top',
            field=models.BooleanField(default=False),
        ),
    ]