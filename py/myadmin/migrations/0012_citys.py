# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-04 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0011_auto_20180702_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('upid', models.IntegerField()),
            ],
            options={
                'db_table': 'citys',
            },
        ),
    ]
