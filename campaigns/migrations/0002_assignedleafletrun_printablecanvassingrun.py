# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('leafleting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polling', '0002_auto_20150302_2101'),
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedLeafletRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('leaflet_run', models.ForeignKey(to='leafleting.LeafletRun')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrintableCanvassingRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('run_code', models.CharField(max_length=15)),
                ('booked_till', models.DateField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('booked_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('canvass_run', models.ForeignKey(to='leafleting.CanvassRun')),
                ('questionnaire', models.ForeignKey(to='polling.CanvassQuestionaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
