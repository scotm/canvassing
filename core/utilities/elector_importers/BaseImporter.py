__author__ = 'scotm'
from copy import deepcopy
import csv

from core.models import Contact, ElectoralRegistrationOffice
from postcode_locator.models import PostcodeMapping


def process_elector_data(line, mapping):
    line = BaseImporter.change_dictionary(line, mapping)
    try:
        line['postcode_point'] = PostcodeMapping.match_postcode(line['postcode'])
    except PostcodeMapping.DoesNotExist:
        pass
    contact = Contact(**line)
    return contact


class BaseImporter(object):
    mapping = {}
    ero_name = ''

    def __init__(self):
        self.electoral_registration_office = ElectoralRegistrationOffice.objects.get(name=self.ero_name)

    @staticmethod
    def change_dictionary(input_dict, dict_mapping=None, processing_dict=None):
        if not (dict_mapping or processing_dict):
            return deepcopy(input_dict)
        output_dict = {}
        if dict_mapping:
            output_dict.update({dict_mapping[i]: j.strip() for i, j in input_dict.iteritems() if i in dict_mapping})
        if processing_dict:
            output_dict.update({i: j(output_dict.get(i, '')) for i, j in processing_dict.iteritems()})
        return output_dict

    def fill_up_db(self, filename):
        records_written = 0
        with open(filename) as myfile:
            sniff_data = myfile.read(1024)
            myfile.seek(sniff_data.find("\n") + 1)
            reader = csv.DictReader(myfile)
            fieldnames = reader.fieldnames
            data = list(reader)

        # INCOMPLETE - DO NOT USE!
        process_elector_data

        Contact.objects.bulk_create(chunk)
        records_written += len(chunk)
        return records_written


class DundeeImporter(BaseImporter):
    mapping = {"ENO": 'ero_number', "First Names": "first_name", "Initials": "initials", "Surname": "surname",
               "Suffix": "suffix", "Address 1": "address_1", "Address 2": "address_2",
               "Address 3": "address_3", "Address 4": "address_4", "Address 5": "address_5",
               "Address 6": "address_6", "Address 7": "address_7", "Address 8": "address_8",
               "Address 9": "address_9", "Postcode": "postcode", }
    name = 'Dundee/Fife'
