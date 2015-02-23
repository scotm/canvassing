# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('area_code', models.CharField(max_length=3)),
                ('descriptio', models.CharField(max_length=50)),
                ('file_name', models.CharField(max_length=50)),
                ('number', models.FloatField()),
                ('number0', models.FloatField()),
                ('polygon_id', models.FloatField()),
                ('unit_id', models.FloatField()),
                ('code', models.CharField(max_length=9)),
                ('hectares', models.FloatField()),
                ('area', models.FloatField()),
                ('type_code', models.CharField(max_length=2)),
                ('descript0', models.CharField(max_length=25)),
                ('type_cod0', models.CharField(max_length=3)),
                ('descript1', models.CharField(max_length=36)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ward_code', models.CharField(max_length=9)),
                ('ward_name', models.CharField(max_length=56)),
                ('wd14nmw', models.CharField(max_length=45)),
                ('local_authority_code', models.CharField(max_length=9)),
                ('local_authority_name', models.CharField(max_length=28)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
