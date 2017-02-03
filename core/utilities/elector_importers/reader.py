
import csv
from itertools import groupby
from core.models import Domecile, ElectoralRegistrationOffice
from core.utilities.functions import split_dict


class ImporterError(Exception):
    pass


class Importer(object):
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as myfile:
            print("Reading electoral data...")
            reader = csv.DictReader(myfile)
            data = [self.preprocess_dict(x) for x in reader]
            self.data = data
            print("done - %d records read" % len(data))

    @property
    def domeciles(self):
        return DomecileImporter(self.data, self.groupby_key)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type == ImporterError:
            print("WTFISTHISSHIT")

    def __repr__(self):
        return "%s (%s)" % (self.__class__.__name__, self.filename)


class DomecileImporter(object):
    domecile_elements = ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7',
                         'postcode']
    ero_details = {'name': 'City of Edinburgh', 'short_name': 'edinburgh', 'address_1': '17A South Gyle Crescent',
                   'address_2': 'EDINBURGH', 'address_3': '', 'postcode': 'EH12 9FL'}

    def __init__(self, data, groupby_key):
        self.domeciles = []
        self.ero = ElectoralRegistrationOffice.objects.filter(name=self.ero_details['name']).first()
        if not self.ero:
            self.ero = ElectoralRegistrationOffice.objects.create(**self.ero_details)
        for grouper, my_group in groupby(data, key=groupby_key):
            my_group = list(my_group)
            domecile_dict = split_dict(my_group[0], self.domecile_elements)
            domecile_dict['electoral_registration_office'] = self.ero
            domecile_obj, result = Domecile.objects.get_or_create(**domecile_dict)
            self.domeciles.append(domecile_obj)

            # Apply that domecile object to each line in the group
            [line.update({'domecile_obj': domecile_obj}) for line in my_group]
