import json
from random import randint

from core.models import Domecile, Contact
from tests.factories import DomecileFactory, ContactFactory, WardFactory
from tests.testcase import LazyTestCase


class CanvassRunsTest(LazyTestCase):
    def load_data(self):
        for street, postcode in [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'),
                                 ('Thorter Way', 'DD1 3DF'), ]:
            DomecileFactory.create_batch(5, address_4=street, postcode=postcode,
                                         postcode_point__postcode=postcode.replace(' ', ''))
        for domecile in Domecile.objects.all():
            batch = randint(1, 2)
            ContactFactory.create_batch(batch, domecile=domecile)

        self.ward = WardFactory()

    def test_get_addresses(self):
        with self.login():
            response = self.get('get_addresses', {'postcode': 'DD4 6BQ'})
            data = json.loads(response.content)
            self.assertEqual(data['buildings'], Domecile.objects.filter(postcode='DD4 6BQ').count())
            self.assertEqual(data['contacts'], Contact.objects.filter(domecile__postcode='DD4 6BQ').count())

    def test_get_addresses_not_in(self):
        with self.login():
            response = self.get('get_addresses', {'postcode': 'EH6 4SZ'})
            data = json.loads(response.content)
            self.assertEqual(data['buildings'], Domecile.objects.filter(postcode='EH6 4SZ').count())
            self.assertEqual(data['contacts'], Contact.objects.filter(domecile__postcode='EH6 4SZ').count())

    def test_get_addresses_blank(self):
        with self.login():
            response = self.get('get_addresses', {})
            data = json.loads(response.content)
            self.assertFalse(data)

    def test_get_addresses_no_login(self):
        response = self.get('get_addresses', {'postcode': 'DD4 6BQ'})
        self.assertRedirectsTo(response, '/login/?next=/')

    def test_get_domeciles(self):
        with self.login():
            data = {'BBox': '-2.937769889831543,56.4740473445564,-2.9126644134521484,56.47997257534551',
                    'ward': self.ward.pk, 'query_type': 'canvassing'}
            print data
            response = self.get('get_domeciles', data)
            print response.content
