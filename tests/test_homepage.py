from django.test import TestCase

# Create your tests here.
from tests.factories import UserFactory


class HomepageTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)

    def test_homepage(self):
        # Without a logged-in user
        response = self.client.get('/')
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)

    def test_homepage_logged_in(self):
        # With a logged-in user
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get('/')
        self.assertTrue(response.status_code == 200)
