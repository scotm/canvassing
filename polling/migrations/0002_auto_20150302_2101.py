# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printablecanvassingrun',
            name='canvass_run',
        ),
        migrations.RemoveField(
            model_name='printablecanvassingrun',
            name='questionnaire',
        ),
        migrations.DeleteModel(
            name='PrintableCanvassingRun',
        ),
    ]
