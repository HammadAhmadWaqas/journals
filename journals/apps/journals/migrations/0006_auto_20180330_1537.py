# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-30 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0005_auto_20180330_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalaboutpage',
            name='short_description',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]
