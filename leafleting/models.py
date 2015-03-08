from functools import cmp_to_key

from django.core.urlresolvers import reverse
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from core.utilities.domecile_comparisons import domecile_cmp
from core.models import Domecile, Contact


class LeafletRun(models.Model):
    name = models.CharField(max_length=50)
    postcode_points = SortedManyToManyField('postcode_locator.PostcodeMapping')
    notes = models.TextField()

    def domeciles(self):
        return Domecile.objects.filter(postcode_point__in=self.postcode_points.all())

    def count(self):
        return self.domeciles().count()

    def __unicode__(self):
        return self.name


class CanvassRun(LeafletRun):
    def get_domeciles(self):
        for postcode_point in self.postcode_points.all():
            list_of_domeciles = sorted(Domecile.objects.filter(postcode_point=postcode_point),
                                       key=cmp_to_key(domecile_cmp))
            for domecile in list_of_domeciles:
                yield domecile

    def get_absolute_url(self):
        return reverse('canvass_run', args=[self.pk, ])

    def get_contact_count(self):
        return Contact.objects.filter(domecile__postcode_point__in=self.postcode_points.all()).count()
