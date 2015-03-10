# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leafleting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canvassrun',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='leafletrun',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
