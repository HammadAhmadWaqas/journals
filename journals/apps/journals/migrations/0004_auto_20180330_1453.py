# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-30 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0003_auto_20180327_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalaboutpage',
            name='custom_content',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='journalaboutpage',
            name='long_description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='journalaboutpage',
            name='short_description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
