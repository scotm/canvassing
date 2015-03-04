# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):
    dependencies = [
        ('leafleting', '0001_initial'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='leafletrun',
            name='postcode_points',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='postcode_locator.PostcodeMapping'),
            preserve_default=True,
        ),
    ]
