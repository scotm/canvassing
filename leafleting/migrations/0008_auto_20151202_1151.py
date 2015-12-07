# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leafleting', '0007_auto_20151124_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedCanvassRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('booked_from', models.DateField(auto_now=True)),
                ('booked_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='canvassrun',
            name='date_available',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='bookedcanvassrun',
            name='canvass_run',
            field=models.OneToOneField(to='leafleting.CanvassRun'),
        ),
    ]
