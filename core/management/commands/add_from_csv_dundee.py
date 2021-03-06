from __future__ import print_function

import csv
from datetime import date
from itertools import groupby

from django.core.management import BaseCommand

from core.models import Domecile, Contact, ElectoralRegistrationOffice
from core.utilities.functions import split_dict, transform_dict

__author__ = 'scotm'

rename_dict = {'PD': 'pd', 'ENO': 'ero_number', 'Title': 'title', 'First Name': 'first_name', 'Initials': 'initials',
               'Surname': 'surname', 'Suffix': 'suffix', 'Date Of Attainment': 'date_of_attainment',
               'Franchise Flag': 'franchise_flag', 'Address 1': 'address_1',
               'Address 2': 'address_2', 'Address 3': 'address_3', 'Address 4': 'address_4', 'Address 5': 'address_5',
               'Address 6': 'address_6', 'Address 7': 'address_7', 'Address 8': 'address_8', 'Address 9': 'address_9',
               'Postcode': 'postcode', }
domecile_elements = ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7',
                     'address_8', 'address_9', 'postcode', ]
contact_elements = ['pd', 'ero_number', 'title', 'first_name', 'initials', 'surname', 'suffix', 'date_of_attainment',
                    'franchise_flag', ]


def groupby_key(x):
    return tuple(x[y] for y in domecile_elements)


class Command(BaseCommand):
    help = 'Fills up the DB with elector data'
    ero_details = {'name': 'Dundee', 'short_name': 'dundee', 'address_1': '18 City Square', 'address_2': '',
                   'address_3': 'Dundee', 'postcode': 'DD1 9XE'}

    def __init__(self):
        super(Command, self).__init__()
        self.ero = ElectoralRegistrationOffice.objects.filter(name='Dundee').first()
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
            data.sort(key=groupby_key)
            print("done - %d records read" % len(data))

        records_done = 0
        temp_list, error_list = [], []
        for grouper, my_group in groupby(data, key=groupby_key):
            my_group = list(my_group)
            domecile_dict = split_dict(my_group[0], domecile_elements)
            domecile_dict['electoral_registration_office'] = self.ero
            domecile_obj, result = Domecile.objects.get_or_create(**domecile_dict)
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
                    if records_done % 5 == 0:
                        try:
                            print("%d records done - last one %s, %s" % (records_done, contact_obj, domecile_obj))
                        except:
                            pass
                        try:
                            Contact.objects.bulk_create(temp_list)
                        except:
                            error_list += temp_list
                        temp_list = []
        if temp_list:
            try:
                Contact.objects.bulk_create(temp_list)
            except:
                error_list += temp_list

        if error_list:
            for i in error_list:
                try:
                    i.save()
                except:
                    try:
                        print(i)
                    except:
                        pass
