# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_intermediatezone'),
        ('leafleting', '0003_auto_20150320_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvassrun',
            name='intermediate_zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.IntermediateZone', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leafletrun',
            name='intermediate_zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.IntermediateZone', null=True),
            preserve_default=True,
        ),
    ]
