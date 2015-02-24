from core.models import Domecile, Contact, ElectoralRegistrationOffice

__author__ = 'scotm'
import csv

from django.core.management import BaseCommand


rename_dict = {'PD': 'pd',
               'ENO': 'ero_number',
               'Title': 'title',
               'First Names': 'first_name',
               'Initials': 'initials',
               'Surname': 'surname',
               'Suffix': 'suffix',
               'Date of Attainment': 'date_of_attainment',
               'Franchise Flag': 'franchise_flag',
               'Opt Out': 'opt_out',
               'Address 1': 'address_1',
               'Address 2': 'address_2',
               'Address 3': 'address_3',
               'Address 4': 'address_4',
               'Address 5': 'address_5',
               'Address 6': 'address_6',
               'Address 7': 'address_7',
               'Address 8': 'address_8',
               'Address 9': 'address_9',
               'Postcode': 'postcode',
}

domecile_elements = ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7',
                     'address_8', 'address_9', 'postcode', ]

contact_elements = ['pd', 'ero_number', 'title', 'first_name', 'initials', 'surname', 'suffix', 'date_of_attainment',
                    'franchise_flag', 'opt_out', ]


def transform_dict(my_dict, rename_dict):
    renamed_dict = {rename_dict[x]: y for x, y in my_dict.items() if x in rename_dict}
    return renamed_dict


def split_dict(my_dict, list_of_elements):
    return {x: my_dict[x] for x in list_of_elements}


class Command(BaseCommand):
    help = 'Fills up the DB with elector data'

    def __init__(self):
        super(Command, self).__init__()
        self.electoral_registration_office = ElectoralRegistrationOffice.objects.get(name='Dundee')

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=unicode)

    def handle(self, *args, **options):
        print options, args
        filename = args[0]
        with open(filename) as myfile:
            reader = csv.DictReader(myfile)
            data = list(reader)

        for line in data:
            line = transform_dict(line, rename_dict)
            domecile_dict = split_dict(line, domecile_elements)
            domecile_dict['electoral_registration_office'] = self.electoral_registration_office
            domecile_obj = Domecile.objects.filter(**domecile_dict).first()
            if not domecile_obj:
                domecile_obj = Domecile.objects.create(**domecile_dict)
                domecile_obj.save()
            contact_dict = split_dict(line, contact_elements)
            if contact_dict['date_of_attainment']:
                this_date = contact_dict['date_of_attainment'].split('/')
                contact_dict['date_of_attainment'] = this_date[2]+"-"+this_date[1]+"-"+this_date[0]
            else:
                contact_dict['date_of_attainment'] = None
            contact_obj = Contact.objects.filter(ero_number=contact_dict['ero_number'],domecile__electoral_registration_office=self.electoral_registration_office).first()
            if not contact_obj:
                contact_obj = Contact(**contact_dict)
            contact_obj.domecile = domecile_obj
            contact_obj.save()





