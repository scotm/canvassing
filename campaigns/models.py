from datetime import date
from datetime import timedelta
from django.conf import settings
from django.db import models

# Create your models here.
from core.models import Domecile
from leafleting.models import CanvassRun, LeafletRun


class Campaign(models.Model):
    parent_campaign = models.ForeignKey('Campaign', null=True, blank=True)
    name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)

    @staticmethod
    def get_latest_top_level_campaign():
        return Campaign.objects.filter(parent_campaign__isnull=True).order_by('date_added').first()

    def __unicode__(self):
        return "%s - started %s" % (self.name, unicode(self.date_added))


class DownloadFile(models.Model):
    parent_campaign = models.ForeignKey(Campaign)
    short_name = models.CharField(max_length=100)
    description = models.TextField()
    download_path = models.FileField()


class PrintableCanvassingRun(models.Model):
    campaign = models.ForeignKey(Campaign)
    run_code = models.CharField(max_length=15)
    questionnaire = models.ForeignKey('polling.CanvassQuestionaire')
    canvass_run = models.ForeignKey(CanvassRun)
    booked_till = models.DateField(blank=True, null=True)
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    completed = models.BooleanField(default=False)

    def book(self, user, days=10, force=False):
        # Booking defaults to 10 days
        if date.today() > self.booked_till and not force:
            raise Exception("Can't book this till %s." % self.booked_till)
        self.booked_till = date.today() + timedelta(days=10)
        self.booked_by = user
        self.save()


class AssignedLeafletRun(models.Model):
    campaign = models.ForeignKey(Campaign)
    leaflet_run = models.ForeignKey(LeafletRun)
    completed = models.BooleanField(default=False)