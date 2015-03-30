# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ward_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='pd',
            field=models.CharField(max_length=6, db_index=True),
            preserve_default=True,
        ),
    ]
