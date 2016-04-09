# coding=utf-8
from __future__ import print_function

import json
from collections import namedtuple

from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.contrib.gis.utils import LayerMapping

from core.utilities.functions import cast_as_int
from postcode_locator.models import PostcodeMapping

AddressInfo = namedtuple('Person', 'prefix residue suffix')
Residue = namedtuple('Residue', 'number_info domecile')


class PoliticalParty(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class ElectoralRegistrationOffice(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    address_3 = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True)

    def __unicode__(self):
        return self.name


class Domecile(models.Model):
    electoral_registration_office = models.ForeignKey(ElectoralRegistrationOffice)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    address_3 = models.CharField(max_length=100)
    address_4 = models.CharField(max_length=500)
    address_5 = models.CharField(max_length=60)
    address_6 = models.CharField(max_length=60)
    address_7 = models.CharField(max_length=60)
    address_8 = models.CharField(max_length=60)
    address_9 = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=10, db_index=True)
    postcode_point = models.ForeignKey(PostcodeMapping, null=True)

    def __unicode__(self):
        return self.get_address_only() + " " + self.postcode

    def get_address_only(self):
        return ", ".join(filter(bool, (getattr(self, "address_%d" % z) for z in range(1, 10))))

    def save(self, *args, **kwargs):
        self.postcode_point = PostcodeMapping.match_postcode(self.postcode, raise_exceptions=False)
        super(Domecile, self).save(*args, **kwargs)

    @staticmethod
    def get_domeciles(northeast, southwest, region=None, query_type='leafleting'):
        from leafleting.models import LeafletRun, CanvassRun
        # Construct a bounding box
        # http://stackoverflow.com/questions/9466043/geodjango-within-a-ne-sw-box

        bounding_box = Polygon.from_bbox((southwest[0], southwest[1], northeast[0], northeast[1]))
        queryset = Domecile.objects.filter(postcode_point__point__contained=bounding_box)
        if region:
            queryset = queryset.filter(postcode_point__point__within=region.geom)
        if query_type in ['leafleting', 'canvassing']:
            inner_klass = LeafletRun
            if query_type == 'canvassing':
                inner_klass = CanvassRun
            queryset = queryset.exclude(postcode_point__in=inner_klass.objects.filter(
                    postcode_points__point__contained=bounding_box).values_list('postcode_points', flat=True))
        return queryset

    @staticmethod
    def get_postcode_points(*args, **kwargs):
        # return Domecile.get_domeciles(*args, **kwargs).distinct('postcode')
        return [{'postcode': x[0], 'point': [x[1].x, x[1].y]} for x in
                Domecile.get_domeciles(*args, **kwargs).values_list('postcode', 'postcode_point__point').distinct()]

    @staticmethod
    def get_sorted_addresses(postcode):
        return [x.domecile for x in Domecile.get_main_address(postcode).residue]

    @staticmethod
    def get_main_address(postcode):
        # p = PostcodeMapping.match_postcode(postcode)
        queryset = Domecile.objects.filter(postcode=postcode)
        addresses = [Residue(number_info=" ".join([getattr(domecile, "address_%d" % x) for x in range(1, 10) if
                                                   getattr(domecile, "address_%d" % x)]).split(), domecile=domecile)
                     for domecile in queryset]
        if not addresses:
            return
        elif len(addresses) == 1:
            return AddressInfo(prefix='', residue=addresses, suffix=addresses[0].number_info)

        # Get all the common data from the front and back of the address list
        suffix, prefix = [], []

        # While the last word is all the same, store it, and remove them.
        try:
            while all(x.number_info[-1] == addresses[0].number_info[-1] for x in addresses):
                suffix.insert(0, addresses[0].number_info[-1])
                for x in addresses:
                    x.number_info.pop(-1)
        except IndexError:
            pass

        try:
            while all(x.number_info[0] == addresses[0].number_info[0] for x in addresses):
                prefix.insert(0, addresses[0].number_info[0])
                for x in addresses:
                    x.number_info.pop(0)
        except IndexError:
            pass

        # Cast the numbers as integers, so it's consistent and easier to sort.
        for x in addresses:
            for index, y in enumerate(x.number_info):
                x.number_info[index] = cast_as_int(y)

        return AddressInfo(prefix=" ".join(prefix),
                           residue=sorted(addresses, key=lambda x: x.number_info),
                           suffix=" ".join(suffix))

    @staticmethod
    def get_summary_of_postcode(postcode):
        from core.utilities.domecile_comparisons import domecile_list_to_string
        return domecile_list_to_string(Domecile.objects.filter(postcode=postcode))

    def get_contacts(self):
        return self.contact_set.all()


class Contact(models.Model):
    pd = models.CharField(max_length=6, db_index=True)
    ero_number = models.CharField(max_length=10, db_index=True)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10)
    domecile = models.ForeignKey(Domecile)
    date_of_attainment = models.DateField(blank=True, null=True)
    franchise_flag = models.CharField(max_length=5)
    email = models.EmailField(max_length=255, blank=True)
    personal_phone = models.CharField(max_length=20, blank=True)
    opt_out = models.BooleanField(default=False)
    westminster_preference = models.ForeignKey(PoliticalParty, blank=True, null=True, related_name='westminster')
    holyrood_preference_constituency = models.ForeignKey(PoliticalParty, blank=True, null=True,
                                                         related_name='holyrood_constituency')
    holyrood_preference_region = models.ForeignKey(PoliticalParty, blank=True, null=True,
                                                   related_name='holyrood_region')
    council_preference = models.ForeignKey(PoliticalParty, blank=True, null=True, related_name='council')
    european_preference = models.ForeignKey(PoliticalParty, blank=True, null=True, related_name='european')

    def __unicode__(self):
        return " ".join([getattr(self, x) for x in ["first_name", "initials", "surname", "suffix"] if getattr(self, x)])

    def get_address(self):
        return [getattr(self.domecile, x) for x in
                ['address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'address_6', 'address_7', 'address_8',
                 'address_9', ] if getattr(self.domecile, x)]

    def has_signed(self, campaign=None):
        from campaigns.models import Campaign, Signature
        if not campaign:
            campaign = Campaign.get_latest_top_level_campaign()
        return Signature.objects.filter(contact=self, campaign=campaign).exists()


class GeomMixin(object):
    def get_simplified_geom_json(self, simplify_factor=0.00003):
        geom = self.geom.simplify(simplify_factor)
        try:
            geom[0] = [(round(x, 6), round(y, 6)) for x, y in geom[0]]
        except:
            pass
        obj = json.loads(geom.json)
        obj['properties'] = {'code': self.code}
        return json.dumps(obj)

    def centre_point(self):
        centroid = self.geom.centroid
        return centroid.y, centroid.x


class Ward(GeomMixin, models.Model):
    # Based on the ward shape files available from:
    # https://geoportal.statistics.gov.uk/Docs/Boundaries/Wards_(GB)_2014_Boundaries_(Full_Extent).zip

    ward_code = models.CharField(max_length=9)
    ward_name = models.CharField(max_length=56)
    wd14nmw = models.CharField(max_length=45, blank=True)
    local_authority_code = models.CharField(max_length=9)
    local_authority_name = models.CharField(max_length=28)
    active = models.BooleanField(default=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    mapping = {'ward_code': 'WD14CD', 'ward_name': 'WD14NM', 'wd14nmw': 'WD14NMW', 'local_authority_code': 'LAD14CD',
               'local_authority_name': 'LAD14NM', 'geom': 'MULTIPOLYGON',}

    class Meta:
        ordering = ('local_authority_name', 'ward_name',)

    def __unicode__(self):
        return "%s: %s" % (self.ward_name, self.local_authority_name)

    @property
    def name(self):
        return self.ward_name

    @property
    def code(self):
        return self.ward_code

    @staticmethod
    def fill_up_db(shapefile, verbose=False):
        lm = LayerMapping(Ward, shapefile, Ward.mapping, transform=True, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)

        print("Removing the non-Scottish wards")
        Ward.objects.exclude(local_authority_code__startswith="S").delete()


class Region(GeomMixin, models.Model):
    # Data based on the Boundary-Line™ program from OS Open Data
    # https://www.ordnancesurvey.co.uk/opendatadownload/products.html
    name = models.CharField(max_length=60)
    area_code = models.CharField(max_length=3)
    description = models.CharField(max_length=50)
    file_name = models.CharField(max_length=50)
    number = models.FloatField()
    number0 = models.FloatField()
    polygon_id = models.FloatField()
    unit_id = models.FloatField()
    code = models.CharField(max_length=9)
    hectares = models.FloatField()
    area = models.FloatField()
    type_code = models.CharField(max_length=2)
    descript0 = models.CharField(max_length=25)
    type_cod0 = models.CharField(max_length=3, blank=True)
    descript1 = models.CharField(max_length=36, blank=True)
    active = models.BooleanField(default=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    mapping = {'name': 'NAME', 'area_code': 'AREA_CODE', 'description': 'DESCRIPTIO', 'file_name': 'FILE_NAME',
               'number': 'NUMBER', 'number0': 'NUMBER0', 'polygon_id': 'POLYGON_ID', 'unit_id': 'UNIT_ID',
               'code': 'CODE', 'hectares': 'HECTARES', 'area': 'AREA', 'type_code': 'TYPE_CODE',
               'descript0': 'DESCRIPT0', 'type_cod0': 'TYPE_COD0', 'descript1': 'DESCRIPT1', 'geom': 'POLYGON',}

    class Meta:
        ordering = ('description', 'name',)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)

    @staticmethod
    def fill_up_db(shapefile, verbose=False):
        lm = LayerMapping(Region, shapefile, Region.mapping, transform=True, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)
        print("Regions imported")
        for i in Region.objects.all():
            i.name = i.name.replace(" P Const", '').replace(" PER", '').replace(" Co Const", '').replace(" Burgh Const",
                                                                                                         '')
            i.save(update_fields=['name'])


class IntermediateZone(GeomMixin, models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=12)
    council_are = models.CharField(max_length=9)
    local_authority_name = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('local_authority_name', 'name',)

    mapping = {
        'code': 'IZ_CODE',
        'name': 'IZ_NAME',
        'council_are': 'CouncilAre',
        'local_authority_name': 'NRSCouncil',
        'geom': 'MULTIPOLYGON',
    }

    def __unicode__(self):
        return "%s: %s" % (self.name, self.local_authority_name)

    @staticmethod
    def fill_up_db(shapefile, verbose=False):
        lm = LayerMapping(IntermediateZone, shapefile, IntermediateZone.mapping, transform=True, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)
        print("Regions imported")


class DataZone(models.Model):
    code = models.CharField(max_length=12)
    name = models.CharField(max_length=110)
    gaelic = models.CharField(max_length=110)
    council_are = models.CharField(max_length=9)
    intermedia = models.CharField(max_length=9)
    councila_2 = models.CharField(max_length=254)
    nrscouncil = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    # Auto-generated `LayerMapping` dictionary for DataZone model
    mapping = {
        'code': 'DZ_CODE',
        'name': 'DZ_NAME',
        'gaelic': 'DZ_GAELIC',
        'council_are': 'CouncilAre',
        'intermedia': 'Intermedia',
        'councila_2': 'CouncilA_2',
        'nrscouncil': 'NRSCouncil',
        'geom': 'MULTIPOLYGON',
    }

    def __unicode__(self):
        if self.name:
            return "%s: %s" % (self.code, self.name)
        else:
            return "%s: %s" % (self.code, self.councila_2)

    @staticmethod
    def fill_up_db(shapefile, verbose=False):
        lm = LayerMapping(DataZone, shapefile, DataZone.mapping, transform=True, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)
        print("Regions imported")
        for i in DataZone.objects.filter(name=''):
            try:
                i.name = IntermediateZone.objects.get(code=i.intermedia).name
                print(i.name)
                i.save()
            except IntermediateZone.DoesNotExist:
                pass


class DataZoneSIMDInfo(models.Model):
    datazone = models.OneToOneField(DataZone, related_name='info', db_index=True)
    population = models.IntegerField(blank=True, null=True)
    working_age_population = models.IntegerField(blank=True, null=True)
    simd_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    simd_rank = models.IntegerField(blank=True, null=True, db_index=True)
    income_deprived_percent = models.FloatField(blank=True, null=True)
    income_deprived_persons = models.IntegerField(blank=True, null=True)
    income_rank = models.IntegerField(blank=True, null=True)
    employment_claimant_percent = models.FloatField(blank=True, null=True)
    employment_claimant_persons = models.IntegerField(blank=True, null=True)
    employment_rank = models.IntegerField(blank=True, null=True)
    standard_mortality_ratio = models.IntegerField(blank=True, null=True)
    comparative_illness_factor = models.IntegerField(blank=True, null=True)
    alcohol_misuse_hospital = models.IntegerField(blank=True, null=True)
    drug_misuse_hospital = models.IntegerField(blank=True, null=True)
    emergency_hospital_stays = models.IntegerField(blank=True, null=True)
    mental_health_medications = models.FloatField(blank=True, null=True)
    low_birth_weight_proportion = models.FloatField(blank=True, null=True)
    health_score = models.FloatField(blank=True, null=True)
    health_rank = models.IntegerField(blank=True, null=True)
    no_qualifications = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neets = models.IntegerField(blank=True, null=True)
    higher_education_proportion_17_21 = models.FloatField(blank=True, null=True)
    pupil_absences = models.FloatField(blank=True, null=True)
    pupil_performance = models.IntegerField(blank=True, null=True)
    education_score = models.FloatField(blank=True, null=True)
    education_rank = models.IntegerField(blank=True, null=True)
    no_central_heating_percent = models.FloatField(blank=True, null=True)
    overcrowded_percent = models.FloatField(blank=True, null=True)
    housing_score = models.FloatField(blank=True, null=True)
    housing_rank = models.IntegerField(blank=True, null=True)
    drive_time_2012_rank = models.IntegerField(blank=True, null=True)
    public_transport_2012_rank = models.IntegerField(blank=True, null=True)
    gp_drive_time_2012 = models.FloatField(blank=True, null=True)
    petrol_drive_time_2012 = models.FloatField(blank=True, null=True)
    post_office_drive_time_2012 = models.FloatField(blank=True, null=True)
    primary_school_drive_time_2012 = models.FloatField(blank=True, null=True)
    secondary_school_drive_time_2012 = models.FloatField(blank=True, null=True)
    retail_centre_drive_time_2012 = models.FloatField(blank=True, null=True)
    gp_public_transport_time_2012 = models.FloatField(blank=True, null=True)
    post_office_public_transport_time_2012 = models.FloatField(blank=True, null=True)
    retail_centre_public_transport_time_2012 = models.FloatField(blank=True, null=True)
    access_to_service_score = models.FloatField(blank=True, null=True)
    access_to_service_rank = models.IntegerField(blank=True, null=True)
    recorded_offences_count = models.IntegerField(blank=True, null=True)
    recorded_offences_per_10000 = models.IntegerField(blank=True, null=True)
    crime_score = models.FloatField(blank=True, null=True)
    crime_rank = models.IntegerField(blank=True, null=True)
