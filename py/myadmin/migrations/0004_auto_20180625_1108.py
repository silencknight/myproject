# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='types',
            name='typename',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
