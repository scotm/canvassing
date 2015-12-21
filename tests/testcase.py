"""
Adapted from: https://gist.github.com/teserak/1363418
Decrease the verbosity of writing view tests.
Old way:
    self.client.get(reverse("my-view"))
    self.client.post(reverse("my-view"), data={"key": "value"})
    self.client.login("username", "password")
    self.client.get(reverse("my-other-view"))
    self.client.logout()
    self.client.post(reverse("my-other-view"), data={"key": "value"}
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response["Location"], "http://remoteserver/")
    session = self.client.session
    session["key"] = "value"
    session.save()
New way:
    self.client.get("my-view")
    self.client.post("my-view", data={"key": "value"})
    with self.login("username", "password"):
        self.client.get("my-other-view")
    self.assertRedirectsTo(response, "http://remoteserver/")
    session = self.session
    session["key"] = "value"
    session.save()
By default also patches the template loader and initiates the client session.
"""

from importlib import import_module

import django.template.loader
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template
from django.test import TestCase

from tests.factories import UserFactory


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
                success,
                "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class LazyTestCase(TestCase):
    patch_templates = True

    def login(self, user=None, password=None):
        if not user:
            user = self.user.username
        if not password:
            password = self.user_password
        return login(self, user, password)

    def get(self, url_name, data=None, *args, **kwargs):
        data = data or {}
        return self.client.get(
                reverse(url_name, args=args, kwargs=kwargs), data
        )

    def post(self, url_name, data=None, *args, **kwargs):
        return self.client.post(
                reverse(url_name, args=args, kwargs=kwargs), data
        )

    @property
    def session(self):
        return self.client.session

    def load_data(self):
        return

    def setUp(self):
        self.user_password = 'top_secret'
        self.user = UserFactory(password=self.user_password)

        if self.patch_templates:
            self.get_template = django.template.loader.get_template

            def get_template(*args, **kwargs):
                return Template("")

            django.template.loader.get_template = get_template

        if "django.contrib.sessions" in settings.INSTALLED_APPS:
            # Workaround for https://code.djangoproject.com/ticket/15740
            engine = import_module(settings.SESSION_ENGINE)
            store = engine.SessionStore()
            store.save()
            self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

        self.load_data()

    def tearDown(self):
        if self.patch_templates:
            django.template.loader.get_template = self.get_template

    def assertRedirectsTo(self, response, url):
        """
        Assert that a response redirects to a specific url without trying to
        load the other page.
        """
        self.assertEqual(response.status_code, 302)
        self.assertIn(url, response["Location"])

    def assertMessageCount(self, response, expect_num):
        """
        Asserts that exactly the given number of messages have been sent.
        """

        actual_num = len(response.context['messages'])
        if actual_num != expect_num:
            self.fail('Message count was %d, expected %d' %
                      (actual_num, expect_num))

    def assertMessageContains(self, response, text, level=None, expected_matches=1):
        """
        Asserts that there is exactly one message containing the given text.
        """

        messages = response.context['messages']

        matches = [m for m in messages if text in m.message]

        if len(matches) == expected_matches:
            msg = matches[0]
            if level is not None and msg.level != level:
                self.fail('There was one matching message but with different'
                          'level: %s != %s' % (msg.level, level))

            return

        elif len(matches) == 0:
            messages_str = ", ".join('"%s"' % m for m in messages)
            self.fail('No message contained text "%s", messages were: %s' %
                      (text, messages_str))
        else:
            self.fail('Incorrect number of messages contained text "%s": %s' %
                      (text, ", ".join(('"%s"' % m) for m in matches)))

    def assertMessageNotContains(self, response, text):
        """ Assert that no message contains the given text. """

        messages = response.context['messages']

        matches = [m for m in messages if text in m.message]

        if len(matches) > 0:
            self.fail('Message(s) contained text "%s": %s' %
                      (text, ", ".join(('"%s"' % m) for m in matches)))
