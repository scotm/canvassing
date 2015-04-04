# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ward_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntermediateZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('code', models.CharField(max_length=12)),
                ('council_are', models.CharField(max_length=9)),
                ('local_authority_name', models.CharField(max_length=254)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('local_authority_name', 'name'),
            },
            bases=(core.models.GeomMixin, models.Model),
        ),
    ]
