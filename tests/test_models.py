from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from core.models import Domecile
from tests.factories import UserFactory, ContactFactory


class ModelsTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)

    def test_contact_page(self):
        contact = ContactFactory.create(domecile__postcode='DD2 9XE', domecile__postcode_point__postcode='DD29XE')
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('contact_view', args=[contact.pk]))
        self.assertTrue(response.status_code == 200)
        d = Domecile.get_sorted_addresses(contact.domecile.postcode)
        ContactFactory.create_batch(20)
        self.assertEqual(d, Domecile.get_sorted_addresses(contact.domecile.postcode))

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
