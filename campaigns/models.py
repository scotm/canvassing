from django.db import models

# Create your models here.
from core.models import Domecile


class Campaign(models.Model):
    parent_campaign = models.ForeignKey('Campaign', null=True)
    name = models.CharField(max_length=100)


class DownloadFile(models.Model):
    parent_campaign = models.ForeignKey(Campaign)
    short_name = models.CharField(max_length=100)
    description = models.TextField()
    download_path = models.FileField()


class LeafletDrop(models.Model):
    leaflet = models.ForeignKey(DownloadFile)
    households = models.ManyToManyField(Domecile)