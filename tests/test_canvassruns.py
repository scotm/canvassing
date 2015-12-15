from random import randint

from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from core.models import Domecile
from postcode_locator.models import PostcodeMapping
from tests.factories import UserFactory, ContactFactory, DomecileFactory, CanvassRunFactory


class CanvassRunsTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)
        for street, postcode in [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'),
                                 ('Thorter Way', 'DD1 3DF'), ]:
            DomecileFactory.create_batch(20, address_4=street, postcode=postcode,
                                         postcode_point__postcode=postcode.replace(' ', ''))
        for domecile in Domecile.objects.all():
            batch = randint(1,3)
            ContactFactory.create_batch(batch, domecile=domecile)
        self.canvass_run = CanvassRunFactory(postcode_points=PostcodeMapping.objects.all())

    def test_name(self):
        self.assertIn(unicode(self.canvass_run), ['This is a test', 'Another Test', 'One more test', ])

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
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(self.canvass_run.get_absolute_url())
        self.assertTrue(response.status_code == 200)
