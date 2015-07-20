# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150413_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=110)),
                ('gaelic', models.CharField(max_length=110)),
                ('council_are', models.CharField(max_length=9)),
                ('intermedia', models.CharField(max_length=9)),
                ('councila_2', models.CharField(max_length=254)),
                ('nrscouncil', models.CharField(max_length=254)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.AlterField(
            model_name='region',
            name='descript1',
            field=models.CharField(max_length=36, blank=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='type_cod0',
            field=models.CharField(max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='ward',
            name='wd14nmw',
            field=models.CharField(max_length=45, blank=True),
        ),
    ]
