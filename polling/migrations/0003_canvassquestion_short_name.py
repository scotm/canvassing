# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0002_auto_20151127_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvassquestion',
            name='short_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
