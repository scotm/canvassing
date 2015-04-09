from __future__ import print_function
from core.utilities.functions import split_dict, transform_dict

__author__ = 'scotm'
import csv
from itertools import groupby

from django.core.management import BaseCommand

from datetime import date
from core.models import Domecile, Contact, ElectoralRegistrationOffice
import re

rename_dict = {'PD': 'pd', 'ENO': 'ero_number', 'Title': 'title', 'First Names': 'first_name', 'Initials': 'initials',
               'Surname': 'surname', 'Suffix': 'suffix', 'Date of Attainment': 'date_of_attainment',
               'Franchise Flag': 'franchise_flag', 'Address 1': 'address_1',
               'Address 2': 'address_2', 'Address 3': 'address_3', 'Address 4': 'address_4', 'Address 5': 'address_5',
               'Address 6': 'address_6', 'Address 7': 'address_7', 'postcode':'postcode', }
domecile_elements = ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7',
                     'postcode']
contact_elements = ['pd', 'ero_number', 'title', 'first_name', 'initials', 'surname', 'suffix', 'date_of_attainment',
                    'franchise_flag', ]

postcode_re = re.compile('^EH[0-9]+ [0-9][A-Z]{2}$')


def groupby_key(x):
    try:
        return tuple(x[y] for y in domecile_elements)
    except:
        print(x)
        raise


def preprocess_dict(my_dict):
    for i in range(5, 0, -1):
        address_field = 'Address %d' % i
        if postcode_re.match(my_dict[address_field]):
            my_dict['postcode'] = my_dict[address_field]
            my_dict[address_field] = ''
            break
    else:
        my_dict['postcode'] = ''

    address_pieces = [my_dict["Address %d" % x] for x in range(1,7) if my_dict["Address %d" % x]]
    if address_pieces[0][0].isdigit():
        first_pieces = address_pieces[0].split(" ")
        my_dict['Address 2'] = first_pieces[0]
        my_dict['Address 3'] = " ".join(first_pieces[1:])
        for i, piece in enumerate(address_pieces[1:]):
            my_dict['Address %d' % (i+4)] = piece
    my_dict = transform_dict(my_dict, rename_dict)
    return my_dict


class Command(BaseCommand):
    help = 'Fills up the DB with elector data'
    ero_details = {'name': 'City of Edinburgh', 'short_name': 'edinburgh', 'address_1': '17A South Gyle Crescent',
                   'address_2': 'EDINBURGH',
                   'address_3': '', 'postcode': 'EH12 9FL'}

    def __init__(self):
        super(Command, self).__init__()
        self.ero = ElectoralRegistrationOffice.objects.filter(name='City of Edinburgh').first()
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
            data = [preprocess_dict(x) for x in reader]
            #data.sort(key=groupby_key)
            print("done - %d records read" % len(data))

        records_done = 0
        temp_list = []
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
                    if records_done % 1000 == 0:
                        print("%d records done - last one %s, %s" % (records_done, contact_obj, domecile_obj))
                        Contact.objects.bulk_create(temp_list)
                        temp_list = []
        if temp_list:
            Contact.objects.bulk_create(temp_list)
            print(temp_list)
