from django.db import models
from sortedm2m.fields import SortedManyToManyField

from core.models import Domecile


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
    pass