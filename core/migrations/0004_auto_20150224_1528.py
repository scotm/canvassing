# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150224_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='person',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
    ]
