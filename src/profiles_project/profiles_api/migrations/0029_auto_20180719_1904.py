# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-19 19:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0028_auto_20180719_0510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='user',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
    ]
