# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150302_1541'),
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvassChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('choice', models.CharField(max_length=200)),
                ('contact', models.ForeignKey(to='core.Contact', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassChoicesAvailable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassLongAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('answer', models.TextField()),
                ('contact', models.ForeignKey(to='core.Contact', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('answer', models.CharField(max_length=5, choices=[(b'Scottish Socialist Party', b'SSP'), (b'SNP', b'SNP'), (b'Scottish Labour', b'SLAB'), (b'Scottish Green', b'GRN'), (b'Conservative', b'CON'), (b'Liberal Democrat', b'LD'), (b'Other', b'Other')])),
                ('contact', models.ForeignKey(to='core.Contact', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polling_question', models.CharField(max_length=200)),
                ('ordering', models.IntegerField(null=True)),
                ('type', models.CharField(default=b'binary', max_length=20, choices=[(b'True/False', b'binary'), (b'Multiple-choice', b'choice'), (b'Range', b'range'), (b'Detailed Answer', b'answer')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassQuestionaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('questions', models.ManyToManyField(to='polling.CanvassQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('answer', models.IntegerField()),
                ('contact', models.ForeignKey(to='core.Contact', null=True)),
                ('question', models.ForeignKey(to='polling.CanvassQuestion')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassTrueFalse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('choice', models.NullBooleanField()),
                ('contact', models.ForeignKey(to='core.Contact', null=True)),
                ('question', models.ForeignKey(to='polling.CanvassQuestion')),
            ],
            options={
                'abstract': False,
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
        migrations.AddField(
            model_name='canvassparty',
            name='question',
            field=models.ForeignKey(to='polling.CanvassQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvasslonganswer',
            name='question',
            field=models.ForeignKey(to='polling.CanvassQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvasschoicesavailable',
            name='question',
            field=models.ForeignKey(to='polling.CanvassQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvasschoice',
            name='question',
            field=models.ForeignKey(to='polling.CanvassQuestion'),
            preserve_default=True,
        ),
    ]
