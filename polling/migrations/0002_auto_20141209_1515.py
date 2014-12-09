# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canvassquestionaire',
            name='campaign',
            field=models.ForeignKey(to='campaigns.Campaign'),
            preserve_default=True,
        ),
    ]
