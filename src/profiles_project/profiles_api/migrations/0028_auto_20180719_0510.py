# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-19 05:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0027_action_activity_bucket_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='action',
        ),
        migrations.RemoveField(
            model_name='bucket',
            name='filetype',
        ),
        migrations.DeleteModel(
            name='Bucket',
        ),
    ]
