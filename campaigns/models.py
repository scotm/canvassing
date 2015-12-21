from django.db import models

from leafleting.models import LeafletRun


class Campaign(models.Model):
    parent_campaign = models.ForeignKey('Campaign', null=True, blank=True)
    name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)

    @staticmethod
    def get_latest_top_level_campaign():
        return Campaign.objects.filter(parent_campaign__isnull=True).order_by('-date_added').first()

    def __unicode__(self):
        return "%s" % (self.name)


class DownloadFile(models.Model):
    parent_campaign = models.ForeignKey(Campaign)
    short_name = models.CharField(max_length=100)
    description = models.TextField()
    download_path = models.FileField()


class AssignedLeafletRun(models.Model):
    campaign = models.ForeignKey(Campaign)
    leaflet_run = models.ForeignKey(LeafletRun)
    completed = models.BooleanField(default=False)


class Signature(models.Model):
    contact = models.ForeignKey('core.Contact')
    campaign = models.ForeignKey(Campaign)
