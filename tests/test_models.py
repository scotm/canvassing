# Create your tests here.
from core.models import Domecile
from tests.factories import ContactFactory
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
        self.assertEqual(self.contact.domecile.get_address_only(), "33, Snookit Street, Dundee")
        self.assertTrue(self.contact in self.contact.domecile.get_contacts())
