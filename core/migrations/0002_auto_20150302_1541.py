# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoliticalParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='council_preference',
            field=models.ForeignKey(related_name='council', blank=True, to='core.PoliticalParty', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='european_preference',
            field=models.ForeignKey(related_name='european', blank=True, to='core.PoliticalParty', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='holyrood_preference_constituency',
            field=models.ForeignKey(related_name='holyrood_constituency', blank=True, to='core.PoliticalParty',
                                    null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='holyrood_preference_region',
            field=models.ForeignKey(related_name='holyrood_region', blank=True, to='core.PoliticalParty', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='westminster_preference',
            field=models.ForeignKey(related_name='westminster', blank=True, to='core.PoliticalParty', null=True),
            preserve_default=True,
        ),
    ]
