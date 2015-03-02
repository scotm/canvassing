# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='date_added',
            field=models.DateField(default=datetime.date(2015, 3, 2), auto_now_add=True),
            preserve_default=False,
        ),
    ]
