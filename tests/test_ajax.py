import json
from random import randint

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.models import Domecile, Contact
from tests.factories import UserFactory, DomecileFactory, ContactFactory


class CanvassRunsTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)
        for street, postcode in [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'),
                                 ('Thorter Way', 'DD1 3DF'), ]:
            DomecileFactory.create_batch(5, address_4=street, postcode=postcode,
                                         postcode_point__postcode=postcode.replace(' ', ''))
        for domecile in Domecile.objects.all():
            batch = randint(1, 2)
            ContactFactory.create_batch(batch, domecile=domecile)

    def test_get_addresses(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('get_addresses'), {'postcode': 'DD4 6BQ'})
        data = json.loads(response.content)
        self.assertEqual(data['buildings'], Domecile.objects.filter(postcode='DD4 6BQ').count())
        self.assertEqual(data['contacts'], Contact.objects.filter(domecile__postcode='DD4 6BQ').count())

    def test_get_addresses_not_in(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('get_addresses'), {'postcode': 'EH6 4SZ'})
        data = json.loads(response.content)
        self.assertEqual(data['buildings'], Domecile.objects.filter(postcode='EH6 4SZ').count())
        self.assertEqual(data['contacts'], Contact.objects.filter(domecile__postcode='EH6 4SZ').count())

    def test_get_addresses_blank(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('get_addresses'), {})
        data = json.loads(response.content)
        self.assertFalse(data)

    def test_get_addresses_no_login(self):
        response = self.client.get(reverse('get_addresses'), {'postcode': 'DD4 6BQ'})
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)
