# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAEN_APP', '0002_portfoliolink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talent',
            name='talent',
            field=models.IntegerField(blank=True, choices=[(0, 'Recording'), (1, 'Artist'), (2, 'Producer'), (3, 'Mixer')], null=True),
        ),
    ]