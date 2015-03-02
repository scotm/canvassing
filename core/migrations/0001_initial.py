# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('postcode_locator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pd', models.CharField(max_length=5, db_index=True)),
                ('ero_number', models.IntegerField(db_index=True)),
                ('title', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=100)),
                ('initials', models.CharField(max_length=10)),
                ('surname', models.CharField(max_length=100)),
                ('suffix', models.CharField(max_length=10)),
                ('date_of_attainment', models.DateField(null=True, blank=True)),
                ('franchise_flag', models.CharField(max_length=5)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('personal_phone', models.CharField(max_length=20, blank=True)),
                ('opt_out', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domecile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(max_length=100)),
                ('address_3', models.CharField(max_length=100)),
                ('address_4', models.CharField(max_length=500)),
                ('address_5', models.CharField(max_length=60)),
                ('address_6', models.CharField(max_length=60)),
                ('address_7', models.CharField(max_length=60)),
                ('address_8', models.CharField(max_length=60)),
                ('address_9', models.CharField(max_length=60)),
                ('phone_number', models.CharField(max_length=15, blank=True)),
                ('postcode', models.CharField(max_length=10, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ElectoralRegistrationOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('short_name', models.CharField(max_length=20)),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(max_length=100)),
                ('address_3', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('area_code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=50)),
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
                'ordering': ('local_authority_name', 'ward_name'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='domecile',
            name='electoral_registration_office',
            field=models.ForeignKey(to='core.ElectoralRegistrationOffice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='domecile',
            name='postcode_point',
            field=models.ForeignKey(to='postcode_locator.PostcodeMapping', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='domecile',
            field=models.ForeignKey(to='core.Domecile'),
            preserve_default=True,
        ),
    ]
