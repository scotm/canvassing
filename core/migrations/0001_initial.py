# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postcode_locator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ero_number', models.IntegerField()),
                ('title', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=100)),
                ('initials', models.CharField(max_length=10)),
                ('surname', models.CharField(max_length=100)),
                ('suffix', models.CharField(max_length=10)),
                ('opt_out', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField()),
                ('person', models.ForeignKey(to='core.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domecile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(max_length=100)),
                ('address_3', models.CharField(max_length=100)),
                ('address_4', models.CharField(max_length=500)),
                ('address_5', models.CharField(max_length=60)),
                ('address_6', models.CharField(max_length=60)),
                ('address_7', models.CharField(max_length=60)),
                ('address_8', models.CharField(max_length=60)),
                ('address_9', models.CharField(max_length=60)),
                ('phone_number', models.CharField(max_length=15, blank=True)),
                ('postcode', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ElectoralRegistrationOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('short_name', models.CharField(max_length=20)),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(max_length=100)),
                ('address_3', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='domecile',
            name='electoral_registration_office',
            field=models.ForeignKey(to='core.ElectoralRegistrationOffice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='domecile',
            name='postcode_point',
            field=models.ForeignKey(to='postcode_locator.PostcodeMapping'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='domecile',
            field=models.ForeignKey(to='core.Domecile'),
            preserve_default=True,
        ),
    ]
