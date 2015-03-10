# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0001_initial'),
        ('leafleting', '0001_initial'),
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='printablecanvassingrun',
            name='questionnaire',
            field=models.ForeignKey(to='polling.CanvassQuestionaire'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='downloadfile',
            name='parent_campaign',
            field=models.ForeignKey(to='campaigns.Campaign'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='parent_campaign',
            field=models.ForeignKey(blank=True, to='campaigns.Campaign', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedleafletrun',
            name='campaign',
            field=models.ForeignKey(to='campaigns.Campaign'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedleafletrun',
            name='leaflet_run',
            field=models.ForeignKey(to='leafleting.LeafletRun'),
            preserve_default=True,
        ),
    ]
