# Create your tests here.
import mock as mock

from core.models import Domecile
from tests.factories import ContactFactory, DomecileFactory
from tests.testcase import LazyTestCase


class ModelsTest(LazyTestCase):
    def load_data(self):
        self.contact = ContactFactory.create(domecile__address_2='33', domecile__postcode='DD2 9XE',
                                             domecile__postcode_point__postcode='DD29XE')

    def test_contact_page(self):
        with self.login():
            response = self.get('contact_view', None, self.contact.pk)
            self.assertTrue(response.status_code == 200)

    def test_contact_page_no_login(self):
        response = self.get('contact_view', None, self.contact.pk)
        self.assertRedirectsTo(response, '/login/?next=/')

    def test_domecile_lists(self):
        d = Domecile.get_sorted_addresses(self.contact.domecile.postcode)
        ContactFactory.create_batch(5)
        self.assertEqual(d, Domecile.get_sorted_addresses(self.contact.domecile.postcode))

    def test_domecile(self):
        self.assertIn("33, Snookit Street, Dundee", self.contact.domecile.get_address_only())
        self.assertTrue(self.contact in self.contact.domecile.get_contacts())

    def test_get_main_address(self):
        domeciles = DomecileFactory.build_batch(3, address_2='34', postcode='DD2 9XE',
                                                postcode_point__postcode='DD29XE')
        domeciles[0].address_1 = 'Flat 16'
        domeciles[1].address_1 = 'Flat 17'
        domeciles[2].address_1 = 'Flat 18'
        with mock.patch('core.models.Domecile.objects.filter') as my_mock:
            my_mock.return_value = domeciles
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            my_mock.assert_called_with(postcode_point=domeciles[0].postcode_point)
            self.assertEqual(test_result.prefix, 'Flat')
            self.assertEqual(test_result.suffix, '34 Snookit Street Dundee')
            domeciles[0].address_1 = 'Flat'
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            my_mock.assert_called_with(postcode_point=domeciles[0].postcode_point)
            self.assertEqual(test_result.prefix, 'Flat')
            self.assertEqual(test_result.suffix, '34 Snookit Street Dundee')
            domeciles[2].address_2 = '33'
            test_result = Domecile.get_main_address(domeciles[0].postcode)
            my_mock.assert_called_with(postcode_point=domeciles[0].postcode_point)
            self.assertEqual(test_result.prefix, 'Flat')
            self.assertEqual(test_result.suffix, 'Snookit Street Dundee')

