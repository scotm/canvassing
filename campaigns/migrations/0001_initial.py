# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leafleting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedLeafletRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DownloadFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('download_path', models.FileField(upload_to=b'')),
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
                ('preserved_canvass_run', jsonfield.fields.JSONField()),
                ('booked_till', models.DateField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('booked_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('canvass_run', models.ForeignKey(to='leafleting.CanvassRun')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
