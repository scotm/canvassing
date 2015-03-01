from __future__ import print_function

__author__ = 'scotm'
import csv
from itertools import groupby

from django.core.management import BaseCommand

from datetime import date
from core.models import Domecile, Contact, ElectoralRegistrationOffice


rename_dict = {'PD': 'pd', 'ENO': 'ero_number', 'Title': 'title', 'First Names': 'first_name', 'Initials': 'initials',
               'Surname': 'surname', 'Suffix': 'suffix', 'Date of Attainment': 'date_of_attainment',
               'Franchise Flag': 'franchise_flag', 'Opt Out': 'opt_out', 'Address 1': 'address_1',
               'Address 2': 'address_2', 'Address 3': 'address_3', 'Address 4': 'address_4', 'Address 5': 'address_5',
               'Address 6': 'address_6', 'Address 7': 'address_7', 'Address 8': 'address_8', 'Address 9': 'address_9',
               'Postcode': 'postcode', }
domecile_elements = ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7',
                     'address_8', 'address_9', 'postcode', ]
contact_elements = ['pd', 'ero_number', 'title', 'first_name', 'initials', 'surname', 'suffix', 'date_of_attainment',
                    'franchise_flag', 'opt_out', ]


def transform_dict(my_dict, rename_dict):
    renamed_dict = {rename_dict[x]: y for x, y in my_dict.items() if x in rename_dict}
    return renamed_dict


def split_dict(my_dict, my_list):
    return {x: my_dict[x] for x in my_list}


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
        filename = args[0]
        with open(filename) as myfile:
            print("Reading electoral data...")
            reader = csv.DictReader(myfile)
            data = [transform_dict(x, rename_dict) for x in reader]
            data.sort(key=groupby_key)
            print("done - %d records read" % len(data))

        records_done = 0
        temp_list = []
        for grouper, my_group in groupby(data, key=groupby_key):
            my_group = list(my_group)
            domecile_dict = split_dict(my_group[0], domecile_elements)
            domecile_dict['electoral_registration_office'] = self.ero
            domecile_obj = Domecile.objects.filter(**domecile_dict).first()
            if not domecile_obj:
                domecile_obj = Domecile.objects.create(**domecile_dict)
                domecile_obj.save()
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





