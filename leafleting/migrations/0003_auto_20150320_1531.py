# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_ward_active'),
        ('leafleting', '0002_auto_20150310_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='canvassrun',
            options={'ordering': ('-pk',)},
        ),
        migrations.AlterModelOptions(
            name='leafletrun',
            options={'ordering': ('-pk',)},
        ),
        migrations.AddField(
            model_name='canvassrun',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvassrun',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.Ward', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leafletrun',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leafletrun',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.Ward', null=True),
            preserve_default=True,
        ),
    ]
