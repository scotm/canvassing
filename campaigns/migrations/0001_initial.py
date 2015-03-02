# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('parent_campaign', models.ForeignKey(blank=True, to='campaigns.Campaign', null=True)),
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
                ('parent_campaign', models.ForeignKey(to='campaigns.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
