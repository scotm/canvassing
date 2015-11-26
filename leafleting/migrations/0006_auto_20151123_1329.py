# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_counts(apps, schema_editor):
    # Ensure the counts are added to the model.
    CanvassRun = apps.get_model("leafleting", "CanvassRun")
    Domecile = apps.get_model("core", "Domecile")
    Contact = apps.get_model("core", "Contact")

    for run in CanvassRun.objects.all():
        run.count = sum(Domecile.objects.filter(postcode_point=x).count() for x in run.postcode_points.all())
        run.count_people = sum(Contact.objects.filter(domecile__postcode_point=x).count() for x in run.postcode_points.all())
        run.save()


class Migration(migrations.Migration):

    dependencies = [
        ('leafleting', '0005_auto_20151123_1250'),
    ]

    operations = [
        migrations.RunPython(add_counts),
    ]