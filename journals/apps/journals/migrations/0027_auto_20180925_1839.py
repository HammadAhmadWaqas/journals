# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-25 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import upload_validator


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0026_auto_20180907_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpagevisit',
            name='journal_about',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_visits', to='journals.JournalAboutPage'),
        ),
        migrations.AlterField(
            model_name='journaldocument',
            name='file',
            field=models.FileField(upload_to='documents', validators=[upload_validator.FileTypeValidator(allowed_extensions=['.pdf'], allowed_types=['application/pdf'])], verbose_name='PDF document'),
        ),
    ]
