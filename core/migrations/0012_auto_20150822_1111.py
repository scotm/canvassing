# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150724_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='simd_rank',
            field=models.IntegerField(db_index=True, null=True, blank=True),
        ),
    ]
