import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from postcode_locator.tests.factories import PostcodeMappingFactory
from tests.factories import UserFactory, ContactFactory, DomecileFactory, CanvassRunFactory


class CanvassRunsSlimTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)
        self.seconduser = UserFactory(username='scotm', password='pump')
        self.postcodemappings = []
        self.domeciles = []
        for street, postcode in [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'),
                                 ('Thorter Way', 'DD1 3DF'), ]:
            postcodemapping = PostcodeMappingFactory(postcode=postcode.replace(' ', ''))
            self.postcodemappings.append(postcodemapping)
            self.domeciles += DomecileFactory.create_batch(3, address_4=street, postcode=postcode,
                                                           postcode_point=postcodemapping)
        for domecile in self.domeciles:
            ContactFactory(domecile=domecile)
        self.canvass_run = CanvassRunFactory(postcode_points=self.postcodemappings, created_by=self.seconduser)

    def test_name(self):
        self.assertIn(unicode(self.canvass_run), {'This is a test', 'Another Test', 'One more test'})

    def test_url(self):
        self.assertEqual(self.canvass_run.get_absolute_url(), '/canvassing/run/%d' % self.canvass_run.pk)

    def test_get_points(self):
        data = json.loads(self.canvass_run.get_points_json())
        self.assertEqual(len(data['coordinates']), len(self.postcodemappings))
        self.assertEqual(data['type'], 'MultiPoint')

    def test_page_no_login(self):
        response = self.client.get(self.canvass_run.get_absolute_url())
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)

    def test_page_login(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(self.canvass_run.get_absolute_url())
        self.assertTrue(response.status_code == 200)

    def test_print_page_login(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('canvass_run_print', args=(self.canvass_run.pk,)))
        self.assertTrue(response.status_code == 200)

    def test_list_page(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('canvass_list'))
        self.assertTrue(response.status_code == 200)
        self.assertIn(self.canvass_run, response.context['object_list'])

    def test_book_page(self):
        self.client.login(username=self.user.username, password=self.user_password)
        self.canvass_run.book(user=self.user)
        response = self.client.get(reverse('canvass_list'))
        self.assertTrue(response.status_code == 200)
        self.assertIn(self.canvass_run, response.context['object_list'])

    def test_book_page_other_user(self):
        self.client.login(username=self.user.username, password=self.user_password)
        self.canvass_run.book(user=self.seconduser)
        response = self.client.get(reverse('canvass_list'))
        self.assertTrue(response.status_code == 200)
        self.assertNotIn(self.canvass_run, response.context['object_list'])
        # Now unbook
        self.canvass_run.unbook()
        response = self.client.get(reverse('canvass_list'))
        self.assertIn(self.canvass_run, response.context['object_list'])

    def test_archive(self):
        self.client.login(username=self.user.username, password=self.user_password)
        self.canvass_run.archive()
        response = self.client.get(reverse('canvass_list'))
        self.assertTrue(response.status_code == 200)
        self.assertNotIn(self.canvass_run, response.context['object_list'])

    def book_twice(self):
        self.canvass_run.book(user=self.seconduser)
        self.canvass_run.book(user=self.seconduser)

    def book_run(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('canvass_run_book', args=(self.canvass_run.pk,)))
        self.assertTrue(response.status_code == 302)
        self.assertTrue(reverse('canvass_list') in response.url)
        self.assertEqual(unicode(self.canvass_run.bookedcanvassrun), "'%s' has been booked by user: john" % unicode(self.canvass_run))