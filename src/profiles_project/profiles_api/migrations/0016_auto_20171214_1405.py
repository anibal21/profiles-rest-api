# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0015_userfile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprocesshistory',
            name='full_storage',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='userprocesshistory',
            name='remaining_storage_doc',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='userprocesshistory',
            name='remaining_storage_image',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='userprocesshistory',
            name='remaining_storage_music',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='userprocesshistory',
            name='remaining_storage_video',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
    ]
