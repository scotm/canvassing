from functools import cmp_to_key

from django.contrib.gis.geos import MultiPoint
from django.core.urlresolvers import reverse
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from core.utilities.domecile_comparisons import domecile_cmp
from core.models import Domecile


class BaseRun(models.Model):
    name = models.CharField(max_length=100)
    postcode_points = SortedManyToManyField('postcode_locator.PostcodeMapping')
    notes = models.TextField()

    class Meta:
        abstract = True

    def get_domeciles(self):
        for postcode_point in self.postcode_points.all():
            list_of_domeciles = sorted(Domecile.objects.filter(postcode_point=postcode_point).prefetch_related('contact_set'),
                                       key=cmp_to_key(domecile_cmp))
            for domecile in list_of_domeciles:
                yield domecile

    def count(self):
        return sum(Domecile.objects.filter(postcode_point=x).count() for x in self.postcode_points.all())

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(self.url_name, args=[self.pk, ])

    def get_points_json(self):
        points = MultiPoint([x.point for x in self.postcode_points.all()])
        return points.json


class LeafletRun(BaseRun):
    url_name = 'leaflet_run'


class CanvassRun(BaseRun):
    url_name = 'canvass_run'

