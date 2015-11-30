# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canvassquestion',
            name='ordering',
        ),
        AlterSortedManyToManyField(
            model_name='canvassquestionaire',
            name='questions',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='polling.CanvassQuestion'),
        ),
    ]
