# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-29 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0008_auto_20171129_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
