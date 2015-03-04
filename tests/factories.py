__author__ = 'scotm'
from random import randint
from datetime import date

import factory
from factory import fuzzy
from django.contrib.auth.models import User, Group

from postcode_locator.tests.factories import PostcodeMappingFactory
from core.models import Contact, Domecile, ElectoralRegistrationOffice

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

    address_1 = ''
    address_2 = '%d' % randint(1,40)
    address_3 = ''
    address_4 = 'Snookit Street'
    address_5 = ''
    address_6 = 'Dundee'
    address_7 = ''
    address_8 = ''
    address_9 = ''
    postcode = ''
    postcode_point = factory.SubFactory(PostcodeMappingFactory)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'john'
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = True
    is_active = True


class SuperuserFactory(UserFactory):
    is_superuser = True


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = "Regional Organisers"


# class MemberFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = Member
#
#     salutation = 'Mr'
#     first_name = "John"
#     last_name = "Doe"
#     email = factory.Sequence(lambda n: 'user%d@gmail.com' % n)
#     date_of_birth = fuzzy.FuzzyDate(date(1940, 1, 1), date(1999, 12, 31))
#     full_name = factory.LazyAttribute(lambda obj: '%s %s' % (obj.first_name, obj.last_name))
#     gender = factory.LazyAttribute(lambda obj: 'Male' if obj.salutation == 'Mr' else 'Female')
#
#     address_line_1 = '1 FalseAddress'
#     address_line_2 = 'No Country'
#     address_line_3 = ''
#     county = 'Glasgow'
#     postcode = 'G32 7PW'
#     telephone_number = '07886794233'
#     branch_assigned = None