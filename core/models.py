# coding=utf-8
from __future__ import print_function
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

from postcode_locator.models import PostcodeMapping


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
        return ", ".join(getattr(self, x) for x in
                         ["address_1", "address_2", "address_3", "address_4", "address_5", "address_6", "address_7",
                          "address_8", "address_9", "postcode"] if getattr(self, x))

    def save(self, *args, **kwargs):
        self.postcode_point = PostcodeMapping.match_postcode(self.postcode, raise_exceptions=False)
        super(Domecile, self).save(*args, **kwargs)

    @staticmethod
    def get_domeciles(northeast, southwest, region=None):
        from django.contrib.gis.geos import Polygon
        # Construct a bounding box
        # http://stackoverflow.com/questions/9466043/geodjango-within-a-ne-sw-box
        geom = Polygon.from_bbox((southwest[0], southwest[1], northeast[0], northeast[1]))
        queryset = Domecile.objects.filter(postcode_point__point__contained=geom)
        if region:
            queryset = queryset.filter(postcode_point__point__within=region.geom)
        return queryset

    @staticmethod
    def get_postcode_points(*args, **kwargs):
        return Domecile.get_domeciles(*args, **kwargs).distinct('postcode')


class Contact(models.Model):
    pd = models.CharField(max_length=5, db_index=True)
    ero_number = models.IntegerField(db_index=True)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)
    surname = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10)
    domecile = models.ForeignKey(Domecile)
    date_of_attainment = models.DateField(blank=True, null=True)
    franchise_flag = models.CharField(max_length=5)
    email = models.EmailField(max_length=255, blank=True)
    personal_phone = models.CharField(max_length=20, blank=True)
    opt_out = models.BooleanField(default=False)

    def __unicode__(self):
        return " ".join([getattr(self, x) for x in ["first_name", "initials", "surname", "suffix"] if getattr(self, x)])


ward_mapping = {
    'ward_code': 'WD14CD',
    'ward_name': 'WD14NM',
    'wd14nmw': 'WD14NMW',
    'local_authority_code': 'LAD14CD',
    'local_authority_name': 'LAD14NM',
    'geom': 'MULTIPOLYGON',
}


class Ward(models.Model):
    # Based on the ward shape files available from:
    # https://geoportal.statistics.gov.uk/Docs/Boundaries/Wards_(GB)_2014_Boundaries_(Full_Extent).zip

    ward_code = models.CharField(max_length=9)
    ward_name = models.CharField(max_length=56)
    wd14nmw = models.CharField(max_length=45)
    local_authority_code = models.CharField(max_length=9)
    local_authority_name = models.CharField(max_length=28)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    class Meta:
        ordering = ('local_authority_name', 'ward_name',)

    def __unicode__(self):
        return "%s: %s - %s" % (self.ward_code, self.ward_name, self.local_authority_name)

    @staticmethod
    def fill_up_db(shapefile, verbose=False):
        from django.contrib.gis.utils import LayerMapping

        lm = LayerMapping(Ward, shapefile, ward_mapping, transform=True, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)

        # Remove the non-Scottish wards
        Ward.objects.exclude(local_authority_code__startswith="S").delete()

    def get_absolute_url(self):
        return reverse('ward_view', args=[self.pk])

    def centre_point(self):
        centroid = self.geom.centroid
        return centroid.y, centroid.x

    def get_simplified_geom_json(self, simplify_factor=0.00003):
        return self.geom.simplify(simplify_factor).json


region_mapping = {
    'name': 'NAME',
    'area_code': 'AREA_CODE',
    'description': 'DESCRIPTIO',
    'file_name': 'FILE_NAME',
    'number': 'NUMBER',
    'number0': 'NUMBER0',
    'polygon_id': 'POLYGON_ID',
    'unit_id': 'UNIT_ID',
    'code': 'CODE',
    'hectares': 'HECTARES',
    'area': 'AREA',
    'type_code': 'TYPE_CODE',
    'descript0': 'DESCRIPT0',
    'type_cod0': 'TYPE_COD0',
    'descript1': 'DESCRIPT1',
    'geom': 'POLYGON',
}


class Region(models.Model):
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
    type_cod0 = models.CharField(max_length=3)
    descript1 = models.CharField(max_length=36)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)

    @staticmethod
    def fill_up_db(shapefile, verbose=False):
        from django.contrib.gis.utils import LayerMapping

        lm = LayerMapping(Region, shapefile, region_mapping, transform=True, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)
        print("Regions imported")
        for i in Region.objects.all():
            i.name = i.name.replace(" P Const", '').replace(" PER", '').replace(" Co Const", '').replace(" Burgh Const",
                                                                                                         '')
            i.save(update_fields=['name'])

    @staticmethod
    def clean_up():
        # We're only interested in Scottish constituencies - so delete the rest - their code begins with an "S".
        Region.objects.exclude(code__startswith="S").delete()

        print("Cleaning up the Highlands and Islands electoral region")
        # The Highlands and Islands electoral region is a massive pain in the arse.
        # Many, many pieces, small islands and areas - hardly any of them usable.
        highlands_regions = Region.objects.filter(name='Highlands and Islands')

        # Prune out the islands without postcode points.
        no_postcode_pks = [region.pk for region in highlands_regions if
                                not PostcodeMapping.objects.filter(point__within=region.geom).exists()]
        Region.objects.filter(pk__in=no_postcode_pks).delete()
        print("Deleted those without postcodes")

        print("Unifying Highlands & Islands geometry...")
        highlands = Region.objects.filter(name='Highlands and Islands').values_list('geom', flat=True)
        highlands = sorted(highlands, key=lambda x: len(x[0][0]), reverse=True)  # Sort them, so
        keep_separate = highlands.pop(0)  # This one is huge, and will slow down processing of the rest.

        # Process pairs of geometry, join them together and repeat.
        while True:
            new_highlands = []
            while highlands:
                if len(highlands) == 0:
                    break
                if len(highlands) == 1:  # If there's only one left, just add it to the next run
                    new_highlands += highlands.pop()
                    break
                geom1, geom2 = highlands.pop(), highlands.pop()
                new_highlands.append(geom1.union(geom2))
            highlands = new_highlands
            if len(highlands) == 1:  # If there's only one left, we're done.
                break

        highlands = highlands[0].union(keep_separate)  # Now join the huge one to the other ones
        print("done")

        # Simplify the region.
        print("Simplifying the geometry a little, for ease of future computation")

        simplified_highlands = highlands.simplify(0.0005, preserve_topology=True)

        # And save it.
        r = Region(name='Highlands and Islands SIMPLIFIED', description='Scottish Parliament Electoral Region',
                   hectares='4050000', geom=simplified_highlands, number=0.0, number0=0.0, polygon_id=0.0, unit_id=0.0,
                   code='',
                   area=0.0, type_code='', descript0='', type_cod0='', descript1='')
        r.save()

        # Nuke the residue - We've already got a decent geom of it.
        Region.objects.filter(name='Highlands and Islands').delete()



