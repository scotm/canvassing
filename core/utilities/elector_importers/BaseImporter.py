import csv
from copy import deepcopy

from core.models import Contact, ElectoralRegistrationOffice, Domecile

__author__ = 'scotm'


class ImproperlyConfiguredImport(Exception):
    pass


def separate_contacts_and_domiciles(line):
    domecile = {key.replace('Domecile.', ''): y for key, y in line.items() if 'Domecile.' in key}
    try:
        matched = Domecile.objects.get(
            **{key.replace('Domecile.', ''): y for key, y in line.items() if 'Domecile.' in key})
    except Domecile.DoesNotExist:
        matched = Domecile(**domecile)
        matched.save()
    contact = {key.replace('Contact.', ''): y for key, y in line.items() if 'Contact.' in key}
    contact = Contact(**contact)
    contact.domecile = matched
    return contact


class BaseImporter(object):
    mapping = {}
    ero_name = ''
    domeciles = set()

    def __init__(self):
        if not (self.mapping and self.ero_name):
            raise ImproperlyConfiguredImport("The importer needs a mapping object and an ero_name")
        self.electoral_registration_office = ElectoralRegistrationOffice.objects.get(name=self.ero_name)

    @staticmethod
    def change_dictionary(input_dict, dict_mapping=None, processing_dict=None):
        if not (dict_mapping or processing_dict):
            return deepcopy(input_dict)
        output_dict = {}
        if dict_mapping:
            output_dict.update({dict_mapping[i]: j.strip() for i, j in input_dict.items() if i in dict_mapping})
        if processing_dict:
            output_dict.update({i: j(output_dict.get(i, '')) for i, j in processing_dict.items()})
        return output_dict

    def process_elector_data(self, line):
        line = BaseImporter.change_dictionary(line, self.mapping)
        line['Domecile.electoral_registration_office'] = self.electoral_registration_office
        return line

    def fill_up_db(self, filename):
        records_written = 0
        with open(filename) as myfile:
            sniff_data = myfile.read(1024)
            myfile.seek(sniff_data.find("\n") + 1)
            reader = csv.DictReader(myfile)
            fieldnames = reader.fieldnames
            data = list(reader)

        # Preprocess the data
        data = (self.process_elector_data(i) for i in data)

        # Separate the Contacts from Domeciles
        contacts = [separate_contacts_and_domiciles(i) for i in data]

        Contact.objects.bulk_create(contacts)
        records_written += len(contacts)
        return records_written


class DundeeImporter(BaseImporter):
    mapping = {"ENO": 'Contact.ero_number', "First Names": "Contact.first_name", "Initials": "Contact.initials",
               "Surname": "Contact.surname",
               "Suffix": "Contact.suffix", "Address 1": "Domecile.address_1", "Address 2": "Domecile.address_2",
               "Address 3": "Domecile.address_3", "Address 4": "Domecile.address_4", "Address 5": "Domecile.address_5",
               "Address 6": "Domecile.address_6", "Address 7": "Domecile.address_7", "Address 8": "Domecile.address_8",
               "Address 9": "Domecile.address_9", "Postcode": "Domecile.postcode", }
    ero_name = 'Dundee/Fife'

    def __init__(self):
        try:
            super(DundeeImporter, self).__init__()
        except ElectoralRegistrationOffice.DoesNotExist:
            self.electoral_registration_office = ElectoralRegistrationOffice.objects.create(name=self.ero_name)
