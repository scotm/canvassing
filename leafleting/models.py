from django.conf import settings

from django.contrib.gis.geos import MultiPoint
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from sortedm2m.fields import SortedManyToManyField

from core.utilities.domecile_comparisons import domecile_key
from core.models import Domecile, Contact, IntermediateZone, Ward, DataZone


class BaseRun(models.Model):
    name = models.CharField(max_length=100)
    postcode_points = SortedManyToManyField('postcode_locator.PostcodeMapping')
    notes = models.TextField()
    count = models.IntegerField(default=0)
    count_people = models.IntegerField(default=0)
    ward = models.ForeignKey('core.Ward', on_delete=models.SET_NULL, null=True)
    intermediate_zone = models.ForeignKey('core.IntermediateZone', on_delete=models.SET_NULL, null=True)
    datazone = models.ForeignKey('core.DataZone', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    class Meta:
        abstract = True
        ordering = ('-pk',)

    def get_domeciles(self):
        for postcode_point in self.postcode_points.all():
            list_of_domeciles = sorted(
                Domecile.objects.filter(postcode_point=postcode_point).prefetch_related('contact_set'),
                key=domecile_key)
            for domecile in list_of_domeciles:
                yield domecile

    def calc_count(self):
        return sum(Domecile.objects.filter(postcode_point=x).count() for x in self.postcode_points.all())

    def calc_count_people(self):
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

    def get_datazone(self):
        return DataZone.objects.filter(geom__contains=self.get_points().centroid).first()


@receiver(post_save)
def baserun_post_save(sender, instance, created, *args, **kwargs):
    if isinstance(instance, BaseRun) and created == True:
        instance.intermediate_zone = instance.get_zone()
        instance.datazone = instance.get_zone()
        instance.ward = instance.get_ward()
        instance.save()


@receiver(m2m_changed)
def post_save_m2m_baserun(sender, instance, action, reverse, *args, **kwargs):
    if isinstance(instance, BaseRun):
        instance.count = instance.calc_count()
        instance.count_people = instance.calc_count_people()
        instance.save()


class LeafletRun(BaseRun):
    url_name = 'leaflet_run'


class CanvassRun(BaseRun):
    url_name = 'canvass_run'
