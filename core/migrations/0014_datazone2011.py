# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20160409_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataZone2011',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objectid', models.IntegerField()),
                ('datazone', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=65)),
                ('totpop2011', models.IntegerField()),
                ('respop2011', models.IntegerField()),
                ('hhcnt2011', models.IntegerField()),
                ('stdareaha', models.FloatField()),
                ('stdareakm2', models.FloatField()),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
