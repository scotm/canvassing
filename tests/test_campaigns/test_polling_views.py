from tests.factories import ContactFactory
from tests.testcase import LazyTestCase

views_names = ['find_contact', 'get_petition_ajax', 'sign_petition_ajax', ]


class ViewsTest(LazyTestCase):
    def load_data(self):
        pass

    def test_302s(self):
        for name in views_names:
            response = self.get(name)
            self.assertEqual(response.status_code, 302)
            self.assertRedirectsTo(response, '/login/?next=/')

    def test_empty_find_contact(self):
        with self.login():
            response = self.get('find_contact')
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context['object_list'])

    def test_not_in_find_contact(self):
        c = ContactFactory.build()
        with self.login():
            response = self.get('find_contact', {'first_name': c.first_name,
                                                 'last_name': c.surname,
                                                 'postcode': c.domecile.postcode})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context['object_list'])

    def test_found_find_contact(self):
        c = ContactFactory()
        with self.login():
            response = self.get('find_contact', {'first_name': c.first_name,
                                                 'last_name': c.surname,
                                                 'postcode': c.domecile.postcode})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['object_list'])
