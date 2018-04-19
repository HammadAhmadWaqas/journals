# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-30 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_siteconfiguration_discovery_journal_api_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='currency_codes',
            field=models.CharField(default='USD', help_text='Comma separated list of currency codes (from discovery core_currencies table)', max_length=256, verbose_name='Currencies supported for purchase'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='discovery_partner_id',
            field=models.CharField(default='', help_text='The short code of the associated Partner in discovery service (core_partners table)', max_length=6, verbose_name='Discovery service partner short code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='ecommerce_partner_id',
            field=models.CharField(default='', help_text='The short code of the associated Partner in ecommerce service (partner_partners table)', max_length=6, verbose_name='Ecommerce sevice partner short code'),
            preserve_default=False,
        ),
    ]