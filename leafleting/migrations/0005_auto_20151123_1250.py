# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leafleting', '0004_auto_20150326_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvassrun',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='canvassrun',
            name='count_people',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leafletrun',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leafletrun',
            name='count_people',
            field=models.IntegerField(default=0),
        ),
    ]
