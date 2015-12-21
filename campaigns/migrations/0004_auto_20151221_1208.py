# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printablecanvassingrun',
            name='booked_by',
        ),
        migrations.RemoveField(
            model_name='printablecanvassingrun',
            name='campaign',
        ),
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
