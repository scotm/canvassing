from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from tests.factories import UserFactory


class HomepageTest(TestCase):
    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)

    def test_homepage(self):
        # Without a logged-in user
        response = self.client.get(reverse('homepage'))
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)

    def test_homepage_logged_in(self):
        # With a logged-in user
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('homepage'))
        self.assertTrue(response.status_code == 200)

    def test_canvass_homepage(self):
        response = self.client.get(reverse('homepage'))
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login/?next=/' in response.url)

    def test_about_page(self):
        # Without a logged-in user
        response = self.client.get(reverse('about_the_ssp'))
        self.assertTrue(response.status_code == 200)

    def test_about_page_logged_in(self):
        # With a logged-in user
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('about_the_ssp'))
        self.assertTrue(response.status_code == 200)

    def test_bugs_page(self):
        # Without a logged-in user
        response = self.client.get(reverse('bugs'))
        self.assertTrue(response.status_code == 200)

    def test_bugs_page_logged_in(self):
        # With a logged-in user
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(reverse('bugs'))
        self.assertTrue(response.status_code == 200)
