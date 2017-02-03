# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0003_canvassquestion_short_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='canvasschoice',
            options={'ordering': ('-date_added',)},
        ),
        migrations.AlterModelOptions(
            name='canvasslonganswer',
            options={'ordering': ('-date_added',)},
        ),
        migrations.AlterModelOptions(
            name='canvassparty',
            options={'ordering': ('-date_added',)},
        ),
        migrations.AlterModelOptions(
            name='canvassrange',
            options={'ordering': ('-date_added',)},
        ),
        migrations.AlterModelOptions(
            name='canvasstruefalse',
            options={'ordering': ('-date_added',)},
        ),
    ]
