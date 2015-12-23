import json
from datetime import date

from django.core.urlresolvers import reverse
from mock import patch, MagicMock

from leafleting.models import BookedCanvassRun, CanvassRun, LeafletRun
from leafleting.views import parse_post_data, create_answer_objects
from postcode_locator.tests.factories import PostcodeMappingFactory
from tests.factories import UserFactory, ContactFactory, DomecileFactory, CanvassRunFactory, WardFactory, \
    CanvassQuestionaireFactory, CanvassQuestionFactory
from tests.testcase import LazyTestCase


class CanvassRunsSlimTest(LazyTestCase):
    def load_data(self):
        self.seconduser = UserFactory(username='scotm', password='pump')
        self.postcodemappings, self.contacts, self.domeciles = [], [], []
        self.addresses_and_postcodes = [('Lilybank Terrace', 'DD4 6BQ'), ('Graham Place', 'DD4 6EH'), ]
        for street, postcode in self.addresses_and_postcodes:
            postcodemapping = PostcodeMappingFactory(postcode=postcode.replace(' ', ''))
            self.postcodemappings.append(postcodemapping)
            self.domeciles += DomecileFactory.create_batch(2, address_4=street, postcode=postcode,
                                                           postcode_point=postcodemapping)
        for domecile in self.domeciles:
            self.contacts.append(ContactFactory(domecile=domecile))
        self.canvass_run = CanvassRunFactory(postcode_points=self.postcodemappings, created_by=self.seconduser)
        self.ward = WardFactory()

    def test_date(self):
        self.canvass_run.book(self.user)
        self.assertEqual(self.canvass_run.bookedcanvassrun.booked_from, date.today())

    def test_canvassrun_name(self):
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
            self.assertEqual(response.status_code, 200)

    def test_canvass_homepage(self):
        with self.login():
            response = self.get('canvass_homepage')
            self.assertEqual(response.status_code, 200)

    def test_print_page_login(self):
        with self.login():
            response = self.get('canvass_run_print', None, self.canvass_run.pk)
            self.assertEqual(response.status_code, 200)

    def test_list_page(self):
        with self.login():
            response = self.get('canvass_list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.canvass_run, response.context['object_list'])

    def test_book_page(self):
        with self.login():
            self.canvass_run.book(user=self.user)
            response = self.get('canvass_list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.canvass_run, response.context['object_list'])

    def test_book_page_other_user(self):
        self.canvass_run.book(user=self.seconduser)
        with self.login():
            response = self.get('canvass_list')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.canvass_run, response.context['object_list'])
            # Now unbook the canvass run
            self.canvass_run.unbook()
            response = self.get('canvass_list')
            self.assertIn(self.canvass_run, response.context['object_list'])

    def test_archive(self):
        # Archive the run, then:
        # 1) Check the date_available is in the not-inconsiderable future
        # 2) Test to ensure that it's not in the canvass list.
        import datetime
        self.canvass_run.archive()
        self.assertTrue(self.canvass_run.date_available >= datetime.date.today() + datetime.timedelta(days=179))
        with self.login():
            response = self.get('canvass_list')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.canvass_run, response.context['object_list'])

    def test_book_twice(self):
        # Nothing should happen if we book a run twice.
        self.canvass_run.book(user=self.user)
        self.canvass_run.book(user=self.seconduser)
        self.assertEqual(self.canvass_run.booked_by, self.seconduser)

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

    def test_create_canvassrun(self):
        questionaire = CanvassQuestionaireFactory(questions=CanvassQuestionFactory.create_batch(2))
        with self.login():
            data = {'run_name': 'A test run', 'selected_postcodes[]': [x[1] for x in self.addresses_and_postcodes],
                    'run_notes': 'Tenements', 'questionaire': questionaire.pk}
            response = self.post('canvass_run_create', data)
            self.assertEqual(response.status_code, 200)
            returned_data = json.loads(response.content)
            self.assertEqual(returned_data['outcome'], 'success')
            canvassrun = CanvassRun.objects.get(name=data['run_name'])
            self.assertEqual(canvassrun.count_people, len(self.contacts))
            self.assertEqual(canvassrun.count, len(self.domeciles))
            self.assertEqual(canvassrun.questionaire, questionaire)

    def test_create_run_no_postcodes(self):
        with self.login():
            data = {'run_name': 'A test run', 'selected_postcodes[]': [], 'run_notes': 'Tenements'}
            response = self.post('canvass_run_create', data)
            self.assertTrue(response.status_code == 404)

    def test_create_leafletrun(self):
        with self.login():
            data = {'run_name': 'A test run', 'selected_postcodes[]': [x[1] for x in self.addresses_and_postcodes],
                    'run_notes': 'Tenements'}
            response = self.post('leaflet_run_create', data)
            self.assertEqual(response.status_code, 200)
            returned_data = json.loads(response.content)
            self.assertTrue(returned_data['outcome'] == 'success')
            canvassrun = LeafletRun.objects.get(name=data['run_name'])
            self.assertTrue(canvassrun.count_people == len(self.contacts))
            self.assertTrue(canvassrun.count == len(self.domeciles))

    def test_canvass_create_page(self):
        with self.login():
            response = self.get('canvass_ward_view', None, self.ward.pk)
            self.assertEqual(response.status_code, 200)
            self.assertIn('request', response.context)
            self.assertIn('/ward/', response.context['request'].path)

    def test_leaflet_create_page(self):
        with self.login():
            response = self.get('leaflet_ward_view', None, self.ward.pk)
            self.assertEqual(response.status_code, 200)
            self.assertIn('request', response.context)
            self.assertIn('/ward/', response.context['request'].path)

    def test_ward(self):
        self.assertEqual(self.ward.__unicode__(), 'Coldside: Dundee City')
        self.assertEqual(self.ward.name, 'Coldside')
        self.assertEqual(self.ward.code, 'S13002548')
        self.assertEqual(self.ward.centre_point(), (56.47700995995096, -2.9252171516418453))

    def test_parse_post_data(self):
        data = "491706_response=&491707_response=&491708_response=responded&491708_question_1=True" \
               "&491708_question_3=1&491708_notes=asdas"
        output = parse_post_data(data)
        self.assertIn('491708', output)
        self.assertEqual(output, {'491708': {'question_3': '1', 'question_1': 'True', 'notes': 'asdas', 'response': 'responded'}})
        # Contacts that return no response should not be in the output
        self.assertNotIn('491706', output)

    def test_create_answer_objects(self):
        with patch('polling.models.CanvassQuestion.objects.get') as mock_question_get, \
                patch('core.models.Contact.objects.get') as mock_contact:
            data = {'491706': {'question_1': '1', 'question_3': 'True', 'notes': 'asdas', 'response': 'responded'}}
            data2 = {'491706': {'question_3': 'True', 'notes': 'asdas', 'response': 'responded'}}
            mock_contact.return_value = MagicMock()
            mock_question_get.return_value = CanvassQuestionFactory.build(type="True/False")
            with patch('polling.models.CanvassTrueFalse.objects.create') as mock_response:
                delete_values, errors = create_answer_objects(data)
                self.assertEqual(mock_response.call_count, 1)
                self.assertEqual(errors, ['KeyError: 1'])
                delete_values, errors = create_answer_objects(data2)
                self.assertEqual(mock_response.call_count, 2)

            data = {'491708': {'question_3': 'Green', 'response': 'responded'}}
            mock_question_get.return_value = CanvassQuestionFactory.build(type="Multiple-choice")
            with patch('polling.models.CanvassChoice.objects.create') as mock_response:
                delete_values, errors = create_answer_objects(data)
                self.assertEqual(mock_response.call_count, 1)
                self.assertEqual(delete_values, ['491708'])
                self.assertFalse(errors)
