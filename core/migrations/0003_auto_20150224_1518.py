# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_region_ward'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='date_of_attainment',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='franchise_flag',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='pd',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='personal_phone',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
