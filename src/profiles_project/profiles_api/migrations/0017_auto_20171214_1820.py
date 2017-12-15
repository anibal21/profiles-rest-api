# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 18:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0016_auto_20171214_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('price', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('storage', models.IntegerField(default=1)),
                ('detail', models.CharField(default='', max_length=255)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PlanType')),
            ],
        ),
        migrations.RenameField(
            model_name='filetype',
            old_name='state',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='userfile',
            old_name='state',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='state',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='userprocesshistory',
            name='full_storage',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='userprocesshistory',
            name='remaining_storage',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='userprocesshistory',
            name='remaining_storage_doc',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='userprocesshistory',
            name='remaining_storage_image',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='userprocesshistory',
            name='remaining_storage_music',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='userprocesshistory',
            name='remaining_storage_video',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='userplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]