# Create your tests here.
import mock as mock

from core.models import Domecile
from tests.factories import ContactFactory, DomecileFactory
from tests.testcase import LazyTestCase


class ModelsTest(LazyTestCase):
    def load_data(self):
        self.contact = ContactFactory.create(domecile__address_2='33', domecile__postcode='DD2 9XE',
                                             domecile__postcode_point__postcode='DD29XE')


    def test_domecile_lists(self):
        d = Domecile.get_sorted_addresses(self.contact.domecile.postcode)
        ContactFactory.create_batch(5)
        self.assertEqual(d, Domecile.get_sorted_addresses(self.contact.domecile.postcode))

    def test_domecile(self):
        self.assertIn("33, Snookit Street, Dundee", self.contact.domecile.get_address_only())
        self.assertTrue(self.contact in self.contact.domecile.get_contacts())

    def test_get_address_only(self):
        print self.contact.domecile.get_address_only()

