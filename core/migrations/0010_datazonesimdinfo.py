# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150720_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataZoneSIMDInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('population', models.IntegerField(blank=True)),
                ('working_age_population', models.IntegerField(blank=True)),
                ('simd_score', models.DecimalField(max_digits=10, decimal_places=2, blank=True)),
                ('simd_rank', models.IntegerField(blank=True)),
                ('income_deprived_percent', models.FloatField(blank=True)),
                ('income_deprived_persons', models.IntegerField(blank=True)),
                ('income_rank', models.IntegerField(blank=True)),
                ('employment_claimant_percent', models.FloatField(blank=True)),
                ('employment_claimant_persons', models.IntegerField(blank=True)),
                ('employment_rank', models.IntegerField(blank=True)),
                ('standard_mortality_ratio', models.IntegerField(blank=True)),
                ('comparative_illness_factor', models.IntegerField(blank=True)),
                ('alcohol_misuse_hospital', models.IntegerField(blank=True)),
                ('drug_misuse_hospital', models.IntegerField(blank=True)),
                ('emergency_hospital_stays', models.IntegerField(blank=True)),
                ('mental_health_medications', models.FloatField(blank=True)),
                ('low_birth_weight_proportion', models.FloatField(blank=True)),
                ('health_score', models.FloatField(blank=True)),
                ('health_rank', models.IntegerField(blank=True)),
                ('no_qualifications', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('neets', models.IntegerField(blank=True)),
                ('higher_education_proportion_17_21', models.FloatField(blank=True)),
                ('pupil_absences', models.FloatField(blank=True)),
                ('pupil_performance', models.IntegerField(blank=True)),
                ('education_score', models.FloatField(blank=True)),
                ('education_rank', models.IntegerField(blank=True)),
                ('no_central_heating_percent', models.FloatField(blank=True)),
                ('overcrowded_percent', models.FloatField(blank=True)),
                ('housing_score', models.FloatField(blank=True)),
                ('housing_rank', models.IntegerField(blank=True)),
                ('drive_time_2012_rank', models.IntegerField(blank=True)),
                ('public_transport_2012_rank', models.IntegerField(blank=True)),
                ('gp_drive_time_2012', models.FloatField(blank=True)),
                ('petrol_drive_time_2012', models.FloatField(blank=True)),
                ('post_office_drive_time_2012', models.FloatField(blank=True)),
                ('primary_school_drive_time_2012', models.FloatField(blank=True)),
                ('secondary_school_drive_time_2012', models.FloatField(blank=True)),
                ('retail_centre_drive_time_2012', models.FloatField(blank=True)),
                ('gp_public_transport_time_2012', models.FloatField(blank=True)),
                ('post_office_public_transport_time_2012', models.FloatField(blank=True)),
                ('retail_centre_public_transport_time_2012', models.FloatField(blank=True)),
                ('access_to_service_score', models.FloatField(blank=True)),
                ('access_to_service_rank', models.IntegerField(blank=True)),
                ('recorded_offences_count', models.IntegerField(blank=True)),
                ('recorded_offences_per_10000', models.IntegerField(blank=True)),
                ('crime_score', models.FloatField(blank=True)),
                ('crime_rank', models.IntegerField(blank=True)),
                ('datazone', models.OneToOneField(related_name='info', to='core.DataZone')),
            ],
        ),
    ]
