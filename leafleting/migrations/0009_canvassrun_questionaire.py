# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0002_auto_20151127_1923'),
        ('leafleting', '0008_auto_20151202_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvassrun',
            name='questionaire',
            field=models.ForeignKey(to='polling.CanvassQuestionaire', null=True),
        ),
    ]
