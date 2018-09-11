# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-07 17:05
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('theming', '0002_auto_20180809_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitebranding',
            name='footer_links',
            field=jsonfield.fields.JSONField(default=[{'destination_link': 'http://www.example.com/', 'label_text': 'FAQ'}, {'destination_link': 'http://www.example.com/', 'label_text': 'Contact Us'}], help_text='JSON should be in the format:\n                     [\n                       {\n                         "label_text": "Link Name 1",\n                         "destination_link": "link_url_1"\n                       },\n                       {\n                         "label_text": "Link Name 2",\n                         "destination_link": "link_url_2"\n                       },\n                    ]', verbose_name='Footer Links'),
        ),
    ]