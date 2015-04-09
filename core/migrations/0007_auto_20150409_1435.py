# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_region_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('description', 'name')},
        ),
        migrations.AlterField(
            model_name='contact',
            name='initials',
            field=models.CharField(max_length=40),
        ),
    ]
