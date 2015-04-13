# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150409_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='ero_number',
            field=models.CharField(max_length=10, db_index=True),
        ),
    ]
