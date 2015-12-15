from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from core.models import Domecile
from tests.factories import UserFactory, ContactFactory


class ModelsTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)
        self.contact = ContactFactory.create(domecile__address_2='33', domecile__postcode='DD2 9XE',
                                             domecile__postcode_point__postcode='DD29XE')

    def test_contact_page(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('contact_view', args=[self.contact.pk]))
        self.assertTrue(response.status_code == 200)

    def test_contact_page_no_login(self):
        response = self.client.get(reverse('contact_view', args=[self.contact.pk]))
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)

    def test_domecile_lists(self):
        d = Domecile.get_sorted_addresses(self.contact.domecile.postcode)
        ContactFactory.create_batch(20)
        self.assertEqual(d, Domecile.get_sorted_addresses(self.contact.domecile.postcode))

    def test_domecile(self):
        self.assertEqual(self.contact.domecile.get_address_only(), "33, Snookit Street, Dundee")
        self.assertTrue(self.contact in self.contact.domecile.get_contacts())


        # def test_about_page_logged_in(self):
        #     # With a logged-in user
        #     self.client.login(username=self.user.username, password=self.user_password)
        #     response = self.client.get(reverse('about_the_ssp'))
        #     self.assertTrue(response.status_code == 200)
        #
        # def test_bugs_page(self):
        #     # Without a logged-in user
        #     response = self.client.get(reverse('bugs'))
        #     self.assertTrue(response.status_code == 200)
        #
        # def test_bugs_page_logged_in(self):
        #     # With a logged-in user
        #     self.client.login(username=self.user.username, password=self.user_password)
        #     response = self.client.get(reverse('bugs'))
        #     self.assertTrue(response.status_code == 200)
