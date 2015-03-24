# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ward_active'),
        ('campaigns', '0002_auto_20150309_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('contact', models.ForeignKey(to='core.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
