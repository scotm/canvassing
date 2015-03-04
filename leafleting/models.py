from django.db import models


class LeafletRun(models.Model):
    name = models.CharField(max_length=50)
    postcode_points = models.ManyToManyField('postcode_locator.PostcodeMapping')
    notes = models.TextField()

    def count(self):
        from core.models import Domecile

        return Domecile.objects.filter(postcode_point__in=self.postcode_points.all()).count()

    def __unicode__(self):
        return self.name


class CanvassRun(LeafletRun):
    pass