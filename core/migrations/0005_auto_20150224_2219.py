# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150224_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domecile',
            name='postcode_point',
            field=models.ForeignKey(to='postcode_locator.PostcodeMapping', null=True),
            preserve_default=True,
        ),
    ]
