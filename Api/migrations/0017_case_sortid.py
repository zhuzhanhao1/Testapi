# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-16 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0016_auto_20191016_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='sortid',
            field=models.IntegerField(default=1, verbose_name='排序号'),
            preserve_default=False,
        ),
    ]
