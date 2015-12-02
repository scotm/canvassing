from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos import MultiPoint
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import m2m_changed
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


@receiver(m2m_changed)
def post_save_m2m_baserun(sender, instance, action, reverse, *args, **kwargs):
    if isinstance(instance, BaseRun) and instance.postcode_points.all():
        instance.intermediate_zone = instance.get_zone()
        instance.datazone = instance.get_datazone()
        instance.ward = instance.get_ward()
        instance.count = instance.calc_count()
        instance.count_people = instance.calc_count_people()
        instance.save()


class LeafletRun(BaseRun):
    url_name = 'leaflet_run'


class CanvassRun(BaseRun):
    url_name = 'canvass_run'
    date_available = models.DateField(null=True)

    def book(self, user):
        BookedCanvassRun.objects.create(canvass_run=self, booked_by=user)

    def unbook(self):
        BookedCanvassRun.objects.filter(canvass_run=self).delete()

    @staticmethod
    def get_unbooked_available_runs():
        # Get those that are available, and have not yet been booked
        return CanvassRun.objects.filter(Q(date_available__isnull=True) | Q(date_available__gte=date.today()),
                                         bookedcanvassrun__isnull=True)

    def archive(self, days=180):
        # By default, make this run available in six months time.
        self.unbook()
        self.date_available = date.today() + timedelta(days=days)
        self.save()


class BookedCanvassRun(models.Model):
    canvass_run = models.OneToOneField(CanvassRun)
    booked_by = models.ForeignKey(User)
    booked_from = models.DateField(auto_now=True)

    def __unicode__(self):
        return u"'%s' has been booked by user: %s" % (unicode(self.canvass_run), unicode(self.booked_by))
