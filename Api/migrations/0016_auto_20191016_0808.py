# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-16 08:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0015_autocase_sortid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='dataType',
        ),
        migrations.RemoveField(
            model_name='case',
            name='isMust',
        ),
        migrations.RemoveField(
            model_name='case',
            name='parameterName',
        ),
        migrations.RemoveField(
            model_name='case',
            name='parameterThat',
        ),
        migrations.RemoveField(
            model_name='case',
            name='requestType',
        ),
    ]
