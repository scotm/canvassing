# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150822_1111'),
        ('leafleting', '0006_auto_20151123_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvassrun',
            name='datazone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.DataZone', null=True),
        ),
        migrations.AddField(
            model_name='leafletrun',
            name='datazone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.DataZone', null=True),
        ),
    ]
