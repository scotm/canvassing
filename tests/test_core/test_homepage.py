from tests.testcase import LazyTestCase


class HomepageTest(LazyTestCase):
    def test_homepage(self):
        # Without a logged-in user
        response = self.get('homepage')
        self.assertEqual(response.status_code,302)
        self.assertRedirectsTo(response, '/login/?next=/')

    def test_homepage_logged_in(self):
        # With a logged-in user
        with self.login():
            response = self.get('homepage')
            self.assertTrue(response.status_code == 200)

    def test_about_page(self):
        # Without a logged-in user
        response = self.get('about_us')
        self.assertTrue(response.status_code == 200)

    def test_about_page_logged_in(self):
        # With a logged-in user
        with self.login():
            response = self.get('about_us')
            self.assertTrue(response.status_code == 200)

    def test_bugs_page(self):
        # Without a logged-in user
        response = self.get('bugs')
        self.assertTrue(response.status_code == 200)

    def test_bugs_page_logged_in(self):
        # With a logged-in user
        with self.login():
            response = self.get('bugs')
            self.assertTrue(response.status_code == 200)

    def test_leaflet_barepages(self):
        response = self.get('why_leaflet')
        self.assertTrue(response.status_code == 200)

    def test_leaflet_barepages_logged_in(self):
        with self.login():
            response = self.get('why_leaflet')
            self.assertTrue(response.status_code == 200)

    def test_canvass_barepages(self):
        response = self.get('why_canvass')
        self.assertTrue(response.status_code == 200)

    def test_canvass_barepages_logged_in(self):
        with self.login():
            response = self.get('why_canvass')
            self.assertTrue(response.status_code == 200)

    def test_reporting(self):
        with self.login():
            response = self.get('reporting')
            self.assertTrue(response.status_code == 200)

