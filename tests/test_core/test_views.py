from tests.factories import ContactFactory
from tests.testcase import LazyTestCase


class ViewsTest(LazyTestCase):
    def load_data(self):
        self.contact = ContactFactory()

    def test_contact_page(self):
        with self.login():
            response = self.get('contact_view', None, self.contact.pk)
            self.assertTrue(response.status_code == 200)

    def test_contact_page_no_login(self):
        response = self.get('contact_view', None, self.contact.pk)
        self.assertRedirectsTo(response, '/login/?next=/')
