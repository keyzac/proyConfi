# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-17 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/event', verbose_name='imagen'),
        ),
        migrations.AddField(
            model_name='ponent',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/ponents', verbose_name='Imagen'),
        ),
    ]
