from __future__ import print_function
import csv
from itertools import groupby

from django.core.management import BaseCommand

from datetime import datetime
from core.models import Domecile, Contact, ElectoralRegistrationOffice
from core.utilities.functions import split_dict, transform_dict

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
    def split_initials(first_name):
        work_data = first_name.split()
        initials = []
        try:
            while len(work_data[-1]) == 1:
                initials.append(work_data.pop())
        except IndexError:
            return first_name, ""
        if initials:
            initials.reverse()
        initials = " ".join(initials)
        return " ".join(work_data).strip(), initials.strip()

    my_dict['surname'] = my_dict['surname'].replace("(z) ", "").strip()
    my_dict['first_name'], my_dict['initials'] = split_initials(my_dict['first_name'])
    if not my_dict['date_of_attainment']:
        my_dict['date_of_attainment'] = None
    else:
        new_date = my_dict['date_of_attainment'].split("/")
        my_dict['date_of_attainment'] = new_date[2]+"-"+new_date[1]+"-"+new_date[0]
        # print (my_dict['date_of_attainment'])
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
            data = [preprocess_dict(x) for x in reader if x['postcode']]
            # data.sort(key=groupby_key)
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
                if not contact_obj:
                    contact_obj = Contact(**contact)
                    contact_obj.domecile = domecile_obj
                    temp_list.append(contact_obj)
                records_done += 1
                if records_done % 1000 == 0:
                    print("%d records done - last one %s, %s" % (records_done, contact_obj, domecile_obj))
                    Contact.objects.bulk_create(temp_list)
                    temp_list = []
        if temp_list:
            Contact.objects.bulk_create(temp_list)
