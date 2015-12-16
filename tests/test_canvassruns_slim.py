from random import randint

from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from core.models import Domecile
from postcode_locator.models import PostcodeMapping
from tests.factories import UserFactory, ContactFactory, DomecileFactory, CanvassRunFactory


class CanvassRunsSlimTest(TestCase):
    def setUp(self):
        for street, postcode in [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'),
                                 ('Thorter Way', 'DD1 3DF'), ]:
            DomecileFactory.create_batch(5, address_4=street, postcode=postcode,
                                         postcode_point__postcode=postcode.replace(' ', ''))
        for domecile in Domecile.objects.all():
            ContactFactory.create_batch(1, domecile=domecile)
        self.canvass_run = CanvassRunFactory(postcode_points=PostcodeMapping.objects.all())

    def test_name(self):
        self.assertIn(unicode(self.canvass_run), {'This is a test', 'Another Test', 'One more test'})

    def test_url(self):
        self.assertEqual(self.canvass_run.get_absolute_url(), '/canvassing/run/%d' % self.canvass_run.pk)

    def test_get_points(self):
        import json
        data = json.loads(self.canvass_run.get_points_json())
        self.assertEqual(len(data['coordinates']), 3)
        self.assertEqual(data['type'], 'MultiPoint')

    def test_page_no_login(self):
        response = self.client.get(self.canvass_run.get_absolute_url())
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)

    def test_page_login(self):
        user_password = 'top_secret'
        user = UserFactory(password=user_password)
        self.client.login(username=user.username, password=user_password)
        response = self.client.get(self.canvass_run.get_absolute_url())
        self.assertTrue(response.status_code == 200)

    def test_print_page_login(self):
        user_password = 'top_secret'
        user = UserFactory(password=user_password)
        self.client.login(username=user.username, password=user_password)
        response = self.client.get(reverse('canvass_run_print', args=(self.canvass_run.pk,)))
        self.assertTrue(response.status_code == 200)
