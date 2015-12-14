__author__ = 'scotm'
from random import randint, choice

import factory
from factory import fuzzy
from django.contrib.auth.models import User, Group

from postcode_locator.tests.factories import PostcodeMappingFactory
from core.models import Contact, Domecile, ElectoralRegistrationOffice
from .names import male_first_names, female_first_names, last_names

# import logging
# logger = logging.getLogger('factory')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

class EROFactory(factory.DjangoModelFactory):
    class Meta:
        model = ElectoralRegistrationOffice
        django_get_or_create = ('name',)

    name = "Dundee"
    short_name = "dundee"
    address_1 = "blah"
    address_2 = "blah"
    address_3 = "blah"
    postcode = "DD1 9XE"


class DomecileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Domecile
        django_get_or_create = ('address_2', 'address_4', 'address_6',)

    address_1 = ''
    address_2 = factory.LazyAttribute(lambda x: str(randint(1, 40)))
    address_3 = ''
    address_4 = 'Snookit Street'
    address_5 = ''
    address_6 = 'Dundee'
    address_7 = ''
    address_8 = ''
    address_9 = ''
    postcode = 'DD1 9XE'
    postcode_point = factory.SubFactory(PostcodeMappingFactory, postcode=factory.SelfAttribute('..postcode'))
    electoral_registration_office = factory.SubFactory(EROFactory)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'john'
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = True
    is_active = True


class ContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contact

    pd = 'EAC'
    ero_number = factory.Sequence(lambda x: str(x))
    title = fuzzy.FuzzyChoice(['Mr', 'Mr', 'Mr', 'Mrs', 'Ms', 'Miss'])
    first_name = factory.LazyAttribute(
        lambda x: choice(male_first_names) if x.title == 'Mr' else choice(female_first_names))
    surname = fuzzy.FuzzyChoice(last_names)
    domecile = factory.SubFactory(DomecileFactory)
    opt_out = False


class SuperuserFactory(UserFactory):
    is_superuser = True


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = "Regional Organisers"
