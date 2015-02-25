# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postcode_locator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeafletRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('notes', models.TextField()),
                ('postcode_points', models.ManyToManyField(to='postcode_locator.PostcodeMapping')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
