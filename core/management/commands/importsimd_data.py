from __future__ import print_function
import csv
import re
from django.core.management import BaseCommand
from core.models import DataZoneSIMDInfo, DataZone
from core.utilities.functions import transform_dict

regex = re.compile(r'(\-?[0-9]+\.[0-9]*|\-?[0-9]+)')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filenames', nargs='+', type=unicode)

    def handle(self, *args, **options):
        for filename in options['filenames']:
            with open(filename) as myfile:
                print("Reading electoral data...")
                reader = list(csv.DictReader(myfile))

            for k, line in enumerate(reader):
                new_dict = transform_dict(line, rename_dict)
                if k == 0:
                    print(new_dict.keys())
                for i in new_dict:
                    new_dict[i] = new_dict[i].replace(",", '')
                    if not new_dict[i]:
                        new_dict[i] = None
                        continue
                    if 'rank' in i:
                        new_dict[i] = str(int(float(new_dict[i])))
                        continue
                    s = regex.search(new_dict[i])
                    if not s:
                        new_dict[i] = None
                    else:
                        new_dict[i] = s.group(0)

                datazone = DataZone.objects.get(code=line['Data Zone'].strip())
                try:
                    DataZoneSIMDInfo.objects.update_or_create(defaults=new_dict, datazone=datazone)
                except:
                    print(new_dict)
                    pass


rename_dict = {"Total Population (SAPE 2010)": 'population',
               "Best-fit Working Age Population** (men 16-64, women 16-60 SAPE 2010)": 'working_age_population',
               "Overall SIMD 2012 Score": 'simd_score',
               "Overall SIMD 2012 Rank": 'simd_rank',
               "Income domain 2012 rate (%)": 'income_deprived_percent',
               "Number of Income Deprived People 2012": 'income_deprived_persons',
               "Income domain 2012 rank": 'income_rank',
               "Employment domain 2012 rate (%)": 'employment_claimant_percent',
               "Number of Employment Deprived People 2012 ": 'employment_claimant_persons',
               "Employment domain 2012 rank": "employment_rank",
               "Standardised mortality ratio (ISD, 2007-2010)": 'standard_mortality_ratio',
               "Comparative illness factor: standardised ratio (DWP, 2011)2": 'comparative_illness_factor',
               "Hospital stays related to alcohol misuse: standardised ratio\n(ISD, 2007-2010)": 'alcohol_misuse_hospital',
               "Hospital stays related to drug misuse: standardised ratio\n(ISD, 2007-2010)": 'drug_misuse_hospital',
               "Emergency stays in hospital: standardised ratio\n(ISD, 2007-2010)": 'emergency_hospital_stays',
               "Estimated proportion of population being prescribed drugs for anxiety, depression or psychosis\n(ISD, 2010)": 'mental_health_medications',
               "Proportion of live singleton births of low birth weight\n(ISD, 2006-2009)": 'low_birth_weight_proportion',
               "Health domain 2012 score": 'health_score',
               "Health domain 2012 rank": 'health_rank',
               "Working age people with no qualifications (2001)2": 'no_qualifications',
               "People aged 16-19 not in full time education, employment or training rate \n(School Leavers 2009/10-2010-11, DWP 2010 and 2011)": 'neets',
               "Proportion of 17- 21 year olds entering higher education \n(HESA 2008/09-2010/11)3": 'higher_education_proportion_17_21',
               "Pupil Performance on SQA at Stage 4 (SQA, 2008/09-2010/11)5": 'pupil_performance',
               "School Pupil Absences \n(Scottish Government, 2009/10-2010/11)4,5": "pupil_absences",
               "Education, Skills and Training domain 2012 score": 'education_score',
               "Education, Skills and Training domain 2012 rank": 'education_rank',
               "Percentage of household population living in households without central heating (Census, 2001)": 'no_central_heating_percent',
               "Percentage of household population living in households that are overcrowded (Census, 2001)": 'overcrowded_percent',
               "Housing domain score 2004, 2006, 2009 & 2012": 'housing_score',
               "Housing domain rank 2004, 2006, 2009 & 2012": 'housing_rank',
               "Drive times sub-domain 2012 rank": 'drive_time_2012_rank',
               "Public transport sub-domain 2012 rank": 'public_transport_2012_rank',
               "Drive time to GP 2012 (mins)": 'gp_drive_time_2012',
               "Drive time to Petrol Station 2012 (mins)": 'petrol_drive_time_2012',
               "Drive time to Post Office 2012 \n(mins)": 'post_office_drive_time_2012',
               "Drive time to Primary School 2012 (mins)": 'primary_school_drive_time_2012',
               "Drive time to Secondary School 2012 (mins)": 'secondary_school_drive_time_2012',
               "Drive time to retail centre 2012 \n(mins)": 'retail_centre_drive_time_2012',
               "Public transport travel time to GP 2012 (mins)":'gp_public_transport_time_2012',
               "Public transport travel time to Post Office 2012 (mins)": 'post_office_public_transport_time_2012',
               "Public transport travel time to retail centre 2012 (mins)": 'retail_centre_public_transport_time_2012',
               "Geographic Access domain 2012 score": 'access_to_service_score',
               "Geographic Access domain 2012 rank": 'access_to_service_rank',
               "SIMD Crime 2012 count": "recorded_offences_count",
               "SIMD Crimes per 10,000 total population": "recorded_offences_per_10000",
               "SIMD Crime 2012 score": 'crime_score',
               "SIMD Crime 2012 rank": 'crime_rank'}
