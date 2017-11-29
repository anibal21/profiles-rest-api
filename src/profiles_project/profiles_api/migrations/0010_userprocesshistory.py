# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-29 15:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0009_auto_20171129_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProcessHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500, null=True)),
                ('last_mod', models.DateTimeField(auto_now_add=True)),
                ('remaining_storage', models.DecimalField(decimal_places=4, default=0, max_digits=5)),
                ('status', models.IntegerField(default=1)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
