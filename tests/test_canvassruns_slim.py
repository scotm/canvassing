import json
from datetime import date

from django.core.urlresolvers import reverse
from django.db import IntegrityError

from leafleting.models import BookedCanvassRun
from postcode_locator.tests.factories import PostcodeMappingFactory
from tests.factories import UserFactory, ContactFactory, DomecileFactory, CanvassRunFactory, WardFactory
from tests.testcase import LazyTestCase


class CanvassRunsSlimTest(LazyTestCase):
    def load_data(self):
        self.seconduser = UserFactory(username='scotm', password='pump')
        self.postcodemappings = []
        self.domeciles = []
        for street, postcode in [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'), ]:
            postcodemapping = PostcodeMappingFactory(postcode=postcode.replace(' ', ''))
            self.postcodemappings.append(postcodemapping)
            self.domeciles += DomecileFactory.create_batch(2, address_4=street, postcode=postcode,
                                                           postcode_point=postcodemapping)
        for domecile in self.domeciles:
            ContactFactory(domecile=domecile)
        self.canvass_run = CanvassRunFactory(postcode_points=self.postcodemappings, created_by=self.seconduser)
        self.ward = WardFactory()

    def test_date(self):
        self.canvass_run.book(self.user)
        self.assertEqual(self.canvass_run.bookedcanvassrun.booked_from, date.today())

    def test_name(self):
        self.assertIn(unicode(self.canvass_run), {'This is a test', 'Another Test', 'One more test'})

    def test_get_points(self):
        data = json.loads(self.canvass_run.get_points_json())
        self.assertEqual(len(data['coordinates']), len(self.postcodemappings))
        self.assertEqual(data['type'], 'MultiPoint')

    def test_page_no_login(self):
        response = self.client.get(self.canvass_run.get_absolute_url())
        self.assertRedirectsTo(response, '/login/?next=/')

    def test_page_login(self):
        with self.login():
            response = self.get('canvass_run', None, self.canvass_run.pk)
            self.assertTrue(response.status_code == 200)

    def test_canvass_homepage(self):
        with self.login():
            response = self.get('canvass_homepage')
            self.assertTrue(response.status_code == 200)

    def test_print_page_login(self):
        with self.login():
            response = self.get('canvass_run_print', None, self.canvass_run.pk)
            self.assertTrue(response.status_code == 200)

    def test_list_page(self):
        with self.login():
            response = self.get('canvass_list')
            self.assertTrue(response.status_code == 200)
            self.assertIn(self.canvass_run, response.context['object_list'])

    def test_book_page(self):
        with self.login():
            self.canvass_run.book(user=self.user)
            response = self.get('canvass_list')
            self.assertTrue(response.status_code == 200)
            self.assertIn(self.canvass_run, response.context['object_list'])

    def test_book_page_other_user(self):
        self.canvass_run.book(user=self.seconduser)
        with self.login():
            response = self.get('canvass_list')
            self.assertTrue(response.status_code == 200)
            self.assertNotIn(self.canvass_run, response.context['object_list'])
            # Now unbook the canvass run
            self.canvass_run.unbook()
            response = self.get('canvass_list')
            self.assertIn(self.canvass_run, response.context['object_list'])

    def test_archive(self):
        self.canvass_run.archive()
        with self.login():
            response = self.get('canvass_list')
            self.assertTrue(response.status_code == 200)
            self.assertNotIn(self.canvass_run, response.context['object_list'])

    def test_book_twice(self):
        with self.assertRaises(IntegrityError):
            self.canvass_run.book(user=self.seconduser)
            self.canvass_run.book(user=self.seconduser)

    def test_book_run(self):
        with self.login():
            response = self.get('canvass_run_book', None, self.canvass_run.pk)
            self.assertRedirectsTo(response, reverse('canvass_list'))
            self.assertEqual(unicode(self.canvass_run.bookedcanvassrun),
                             "'%s' has been booked by user: john" % unicode(self.canvass_run))

    def test_unbook_run(self):
        self.canvass_run.book(user=self.user)
        with self.login():
            response = self.get('canvass_run_unbook', None, self.canvass_run.pk)
            self.assertRedirectsTo(response, reverse('canvass_list'))
            self.assertFalse(BookedCanvassRun.objects.all())
