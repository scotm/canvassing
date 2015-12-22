import mock as mock
from django.test import TestCase

from core.models import Domecile
from tests.factories import DomecileFactory, PoliticalPartyFactory, EROFactory


class ModelSlim(TestCase):
    def test_get_main_address(self):
        domeciles = DomecileFactory.build_batch(3, address_2='34', postcode='DD2 9XE',
                                                postcode_point__postcode='DD29XE')
        domeciles[0].address_1 = 'Flat 16'
        domeciles[1].address_1 = 'Flat 17'
        domeciles[2].address_1 = 'Flat 18'
        with mock.patch('core.models.Domecile.objects.filter') as my_mock:
            my_mock.return_value = domeciles
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            my_mock.assert_called_with(postcode=domeciles[0].postcode)
            self.assertEqual(test_result.prefix, 'Flat')
            self.assertEqual(test_result.suffix, '34 Snookit Street Dundee')
            domeciles[0].address_1 = 'Flat'
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            self.assertEqual(test_result.prefix, 'Flat')
            self.assertEqual(test_result.suffix, '34 Snookit Street Dundee')
            domeciles[2].address_2 = '33'
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            self.assertEqual(test_result.prefix, 'Flat')
            self.assertEqual(test_result.suffix, 'Snookit Street Dundee')
            domeciles[0].address_1 = ''
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            self.assertEqual(test_result.prefix, '')
            self.assertEqual(test_result.suffix, 'Snookit Street Dundee')

    def test_get_main_address_none(self):
        with mock.patch('core.models.Domecile.objects.filter') as my_mock:
            my_mock.return_value = []
            test_result = Domecile.get_main_address('EH6 4SZ')
            self.assertEqual(test_result, None)
            my_mock.assert_called_with(postcode='EH6 4SZ')

    def test_politicalparty(self):
        party = PoliticalPartyFactory.build()
        self.assertEqual(party.__unicode__(), 'Scottish Socialist Party')

    def test_ero_model(self):
        ero = EROFactory.build()
        self.assertEqual(ero.__unicode__(), 'Dundee')
