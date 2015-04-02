from functools import cmp_to_key

from django.conf import settings
from django.contrib.gis.geos import MultiPoint
from django.core.urlresolvers import reverse
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from core.utilities.domecile_comparisons import domecile_cmp
from core.models import Domecile, Contact, IntermediateZone, Ward


class BaseRun(models.Model):
    name = models.CharField(max_length=100)
    postcode_points = SortedManyToManyField('postcode_locator.PostcodeMapping')
    notes = models.TextField()
    ward = models.ForeignKey('core.Ward', on_delete=models.SET_NULL, null=True)
    intermediate_zone = models.ForeignKey('core.IntermediateZone', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    class Meta:
        abstract = True
        ordering = ('-pk',)

    def save(self, *args, **kwargs):
        # Fix this later
        # self.ward = self.get_ward()
        # self.intermediate_zone = self.get_zone()
        super(BaseRun, self).save(*args, **kwargs)

    def get_domeciles(self):
        for postcode_point in self.postcode_points.all():
            list_of_domeciles = sorted(
                Domecile.objects.filter(postcode_point=postcode_point).prefetch_related('contact_set'),
                key=cmp_to_key(domecile_cmp))
            for domecile in list_of_domeciles:
                yield domecile

    def count(self):
        return sum(Domecile.objects.filter(postcode_point=x).count() for x in self.postcode_points.all())

    def count_people(self):
        return sum(Contact.objects.filter(domecile__postcode_point=x).count() for x in self.postcode_points.all())

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(self.url_name, args=[self.pk, ])

    def get_points(self):
        return MultiPoint([x.point for x in self.postcode_points.all()])

    def get_points_json(self):
        return self.get_points().json

    def get_ward(self):
        return Ward.objects.filter(geom__contains=self.get_points().centroid).first()

    def get_zone(self):
        return IntermediateZone.objects.filter(geom__contains=self.get_points().centroid).first()


class LeafletRun(BaseRun):
    url_name = 'leaflet_run'


class CanvassRun(BaseRun):
    url_name = 'canvass_run'