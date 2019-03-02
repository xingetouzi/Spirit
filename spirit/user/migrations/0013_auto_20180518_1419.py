# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 06:19
from __future__ import unicode_literals

from django.db import migrations, models
import spirit.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0012_auto_20180516_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.png', upload_to=spirit.user.models.upload_article_cover),
        ),
    ]