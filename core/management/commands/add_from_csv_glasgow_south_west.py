from __future__ import print_function
from core.utilities.functions import split_dict, transform_dict

import csv
from itertools import groupby

from django.core.management import BaseCommand

from datetime import datetime
from core.models import Domecile, Contact, ElectoralRegistrationOffice

__author__ = 'scotm'

rename_dict = {'DISTRICT': 'pd', 'ELNO': 'ero_number', 'FORENAMES': 'first_name', 'SURNAME': 'surname',
               'QUALIFICATION': 'franchise_flag', 'DO18': 'date_of_attainment', 'FLAT': 'address_1',
               'HOUSENUMBER': 'address_2', 'STREETNAME': 'address_4', 'SUBSTREETNAME': 'address_5',
               'STREETADD1': 'address_6', 'PCODE': 'postcode', }

domecile_elements = ['address_1', 'address_2', 'address_4', 'address_5', 'address_6', 'postcode', ]
contact_elements = ['pd', 'ero_number', 'first_name', 'surname', 'date_of_attainment', 'franchise_flag', ]


def groupby_key(x):
    return tuple(x[y] for y in domecile_elements)


def preprocess_dict(my_dict):
    address_pieces = my_dict['STREETADD1'].split()
    if address_pieces and address_pieces[0].isnumeric() and my_dict['SUBSTREETNAME'] and not my_dict['HOUSENUMBER']:
        pieces = [x.strip() for x in my_dict['SUBSTREETNAME'].split(',')]
        if pieces[-1].isnumeric() and pieces[-1] == address_pieces[0]:
            my_dict['HOUSENUMBER'] = pieces[-1]
            my_dict['SUBSTREETNAME'] = ", ".join(pieces[:-1])
            my_dict['STREETADD1'] = my_dict['STREETADD2']
            my_dict['STREETADD2'] = ''
    if not my_dict['FLAT'] and my_dict['HOUSENAME']:
        my_dict['FLAT'] = my_dict['HOUSENAME']
    if not my_dict['HOUSENUMBER'] and my_dict['HOUSENAME']:
        my_dict['HOUSENUMBER'] = my_dict['HOUSENAME']
    my_dict['SURNAME'] = my_dict['SURNAME'].replace('(z) ', '')
    my_dict['DO18'] = datetime.strptime(my_dict['DO18'], '%d/%m/%Y').date() if my_dict['DO18'] else None
    my_dict = transform_dict(my_dict, rename_dict)
    return my_dict


class Command(BaseCommand):
    help = 'Fills up the DB with elector data'
    ero_details = {'name': 'Glasgow', 'short_name': 'glasgow', 'address_1': '', 'address_2': '',
                   'address_3': '', 'postcode': ''}

    def __init__(self):
        super(Command, self).__init__()
        self.ero = ElectoralRegistrationOffice.objects.filter(name='Glasgow').first()
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
            data = [preprocess_dict(x) for x in reader if x['PCODE']]
            data.sort(key=groupby_key)
            print("done - %d records read" % len(data))

        records_done = 0
        temp_list = []
        for grouper, my_group in groupby(data, key=groupby_key):
            my_group = list(my_group)
            domecile_dict = split_dict(my_group[0], domecile_elements)
            domecile_dict['electoral_registration_office'] = self.ero
            domecile_obj, result = Domecile.objects.get_or_create(**domecile_dict)
            for line in my_group:
                contact = split_dict(line, contact_elements)
                contact_obj = Contact.objects.filter(ero_number=contact['ero_number'], pd=contact['pd'],
                                                     domecile__electoral_registration_office=self.ero).first()
                records_done += 1
                if not contact_obj:
                    contact_obj = Contact(**contact)
                    contact_obj.domecile = domecile_obj
                    temp_list.append(contact_obj)
                if records_done % 1000 == 0:
                    print("%d records done - last one %s, %s" % (records_done, contact_obj, domecile_obj))
                    Contact.objects.bulk_create(temp_list)
                    temp_list = []
        if temp_list:
            Contact.objects.bulk_create(temp_list)
