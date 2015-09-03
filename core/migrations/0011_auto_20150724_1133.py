# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_datazonesimdinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='access_to_service_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='access_to_service_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='alcohol_misuse_hospital',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='comparative_illness_factor',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='crime_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='crime_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='drive_time_2012_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='drug_misuse_hospital',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='education_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='education_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='emergency_hospital_stays',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='employment_claimant_percent',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='employment_claimant_persons',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='employment_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='gp_drive_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='gp_public_transport_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='health_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='health_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='higher_education_proportion_17_21',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='housing_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='housing_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='income_deprived_percent',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='income_deprived_persons',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='income_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='low_birth_weight_proportion',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='mental_health_medications',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='neets',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='no_central_heating_percent',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='no_qualifications',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='overcrowded_percent',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='petrol_drive_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='population',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='post_office_drive_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='post_office_public_transport_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='primary_school_drive_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='public_transport_2012_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='pupil_absences',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='pupil_performance',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='recorded_offences_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='recorded_offences_per_10000',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='retail_centre_drive_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='retail_centre_public_transport_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='secondary_school_drive_time_2012',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='simd_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='simd_score',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='standard_mortality_ratio',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datazonesimdinfo',
            name='working_age_population',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
