# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150224_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domecile',
            name='postcode',
            field=models.CharField(max_length=10, db_index=True),
            preserve_default=True,
        ),
    ]
