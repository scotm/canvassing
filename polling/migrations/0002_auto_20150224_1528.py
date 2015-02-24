# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150224_1528'),
        ('polling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvassChoicesAvailable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.CharField(max_length=100)),
                ('question', models.ForeignKey(to='polling.CanvassQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanvassTrueFalse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            model_name='canvasschoice',
            name='contact',
            field=models.ForeignKey(to='core.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvasslonganswer',
            name='contact',
            field=models.ForeignKey(to='core.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvassquestion',
            name='type',
            field=models.CharField(default=b'binary', max_length=20, choices=[(b'True/False', b'binary'), (b'Multiple-choice', b'choice'), (b'Detailed Answer', b'answer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canvassquestionaire',
            name='questions',
            field=models.ManyToManyField(to='polling.CanvassQuestion'),
            preserve_default=True,
        ),
    ]
