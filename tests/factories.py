from datetime import date

from campaigns.models import Campaign, DownloadFile, Signature
from leafleting.models import CanvassRun
from leafleting.models import LeafletRun
from polling.models import CanvassQuestion

__author__ = 'scotm'
from random import randint, choice

import factory
from factory import fuzzy
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import Polygon, MultiPolygon

from postcode_locator.tests.factories import PostcodeMappingFactory, northeast, northwest, southeast, southwest
from core.models import Contact, Domecile, ElectoralRegistrationOffice, Ward
from .names import male_first_names, female_first_names, last_names


# import logging
# logger = logging.getLogger('factory')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

class WardFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ward

    ward_code = 'S13002548'
    ward_name = 'Coldside'
    wd14nmw = ''
    local_authority_code = 'S12000042'
    local_authority_name = 'Dundee City'
    active = True
    geom = factory.LazyAttribute(
        lambda x: MultiPolygon(Polygon((northwest, northeast, southeast, southwest, northwest))))


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
    postcode_point = factory.SubFactory(PostcodeMappingFactory, postcode='DD19XE')
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


class CampaignFactory(factory.DjangoModelFactory):
    class Meta:
        model = Campaign
        django_get_or_create = ('parent_campaign', 'name', 'date_added',)

    parent_campaign = None
    name = "Holyrood 2016"
    date_added = date(2015, 12, 15)


class DownloadFileFactory(factory.DjangoModelFactory):
    class Meta:
        model = DownloadFile

    parent_campaign = factory.SubFactory(CampaignFactory)
    short_name = 'A file'
    description = 'A downloadable File'
    download_path = factory.django.FileField()


class SignatureFactory(factory.DjangoModelFactory):
    class Meta:
        model = Signature

    contact = factory.SubFactory(ContactFactory)
    campaign = factory.SubFactory(CampaignFactory)


class LeafletRunFactory(factory.DjangoModelFactory):
    class Meta:
        model = LeafletRun


class CanvassRunFactory(factory.DjangoModelFactory):
    class Meta:
        model = CanvassRun

    name = factory.Iterator(['This is a test', 'Another Test', 'One more test', ])
    notes = 'This is where we note tenements, buzzers and all that'
    count = 0
    count_people = 0

    @factory.post_generation
    def postcode_points(self, create, extracted, **kwargs):
        if create and extracted:
            # A list of points were passed in, use them
            for point in extracted:
                self.postcode_points.add(point)


class CanvassQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = CanvassQuestion

    short_name = factory.Iterator(['Independence', 'Heard of Org', ''])
    polling_question = factory.Iterator(
            ['Should Scotland be an independent country?', 'Have you heard of our organisation?', ''])
    type = factory.Iterator(['True/False', 'True/False'])


class SuperuserFactory(UserFactory):
    is_superuser = True


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = "Regional Organisers"
