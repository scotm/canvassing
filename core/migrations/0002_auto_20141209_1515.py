# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0002_auto_20141209_1515'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='parent_campaign',
        ),
        migrations.RemoveField(
            model_name='downloadfile',
            name='parent_campaign',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
        migrations.RemoveField(
            model_name='leafletdrop',
            name='households',
        ),
        migrations.RemoveField(
            model_name='leafletdrop',
            name='leaflet',
        ),
        migrations.DeleteModel(
            name='DownloadFile',
        ),
        migrations.DeleteModel(
            name='LeafletDrop',
        ),
    ]
