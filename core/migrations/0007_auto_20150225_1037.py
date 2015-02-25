# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150225_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='ero_number',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='pd',
            field=models.CharField(max_length=5, db_index=True),
            preserve_default=True,
        ),
    ]
