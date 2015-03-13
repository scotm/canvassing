# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150302_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='ward',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
