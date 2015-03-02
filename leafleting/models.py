from django.db import models

# Create your models here.
from core.models import Domecile


class LeafletRun(models.Model):
    name = models.CharField(max_length=50)
    postcode_points = models.ManyToManyField('postcode_locator.PostcodeMapping')
    notes = models.TextField()

    def count(self):
        return Domecile.objects.filter(postcode_point__in=self.postcode_points.all()).count()


class CanvassRun(LeafletRun):
    pass