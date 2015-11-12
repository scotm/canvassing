from __future__ import print_function
from core.utilities.functions import split_dict, transform_dict

__author__ = 'scotm'
import csv
from itertools import groupby

from django.core.management import BaseCommand
from django.db.utils import DataError

from datetime import date
from core.models import Domecile, Contact, ElectoralRegistrationOffice


rename_dict = {'PD': 'pd', 'ENO': 'ero_number', 'Title': 'title', 'First Names': 'first_name', 'Initials': 'initials',
               'Surname': 'surname', 'Suffix': 'suffix', 'Date of Attainment': 'date_of_attainment',
               'Franchise Flag': 'franchise_flag', 'Opt Out': 'opt_out', 'Address 1': 'address_1',
               'Address 2': 'address_2', 'Address 3': 'address_3', 'Address 4': 'address_4', 'Address 5': 'address_5',
               'Address 6': 'address_6', 'Address 7': 'address_7', 'Postcode': 'postcode', }
domecile_elements = ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7',
                     'postcode', ]
contact_elements = ['pd', 'ero_number', 'title', 'first_name', 'initials', 'surname', 'suffix', 'date_of_attainment',
                    'franchise_flag', ]


def groupby_key(x):
    return tuple(x[y] for y in domecile_elements)


class Command(BaseCommand):
    help = 'Fills up the DB with elector data'
    ero_details = {'name': 'South Lanarkshire', 'short_name': 's_lanarkshire',
                   'address_1': 'Lanarkshire Valuation Joint Board', 'address_2': 'North Stand, Cadzow Avenue',
                   'address_3': 'Hamilton', 'postcode': 'ML3 0LU'}

    def __init__(self):
        super(Command, self).__init__()
        self.ero = ElectoralRegistrationOffice.objects.filter(name='South Lanarkshire').first()
        if not self.ero:
            self.ero = ElectoralRegistrationOffice(**self.ero_details)
            self.ero.save()

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=unicode)

    def handle(self, *args, **options):
        filename = options['filename'][0]
        with open(filename) as myfile:
            print("Reading electoral data...")
            reader = csv.DictReader(myfile)
            data = [transform_dict(x, rename_dict) for x in reader]
            for line in data:
                if 'postcode' not in line or not line['postcode']:
                    for i in range(7,0,-1):
                        index = 'address_'+str(i)
                        if line[index]:
                            try:
                                line['postcode'] = line['address_'+str(i)]
                                line['address_%d'+str(i)] = ''
                                break
                            except KeyError:
                                line['postcode'] = ''
                                break
                            finally:
                                if line['postcode'] == 'OTHER ELECTORS':
                                    line['postcode'] = ''
            data.sort(key=groupby_key)
            print("done - %d records read" % len(data))

        records_done = 0
        temp_list = []
        for grouper, my_group in groupby(data, key=groupby_key):
            my_group = list(my_group)
            domecile_dict = split_dict(my_group[0], domecile_elements)
            domecile_dict['electoral_registration_office'] = self.ero
            try:
                domecile_obj, result = Domecile.objects.get_or_create(**domecile_dict)
            except DataError:
                print(domecile_dict)
                raise
            for line in my_group:
                contact_dict = split_dict(line, contact_elements)
                if contact_dict['date_of_attainment']:
                    temp = [int(x) for x in contact_dict['date_of_attainment'].split('/')]
                    contact_dict['date_of_attainment'] = date(temp[2], temp[1], temp[0])
                else:
                    contact_dict['date_of_attainment'] = None
                contact_obj = Contact.objects.filter(ero_number=contact_dict['ero_number'],
                                                     domecile__electoral_registration_office=self.ero,
                                                     pd=contact_dict['pd']).first()
                records_done += 1
                if not contact_obj:
                    contact_obj = Contact(**contact_dict)
                    contact_obj.domecile = domecile_obj
                    temp_list.append(contact_obj)
                    if records_done % 1000 == 0:
                        print("%d records done - last one %s, %s" % (records_done, contact_obj, domecile_obj))
                        Contact.objects.bulk_create(temp_list)
                        temp_list = []
        if temp_list:
            Contact.objects.bulk_create(temp_list)
            print(temp_list)
