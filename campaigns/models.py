from django.db import models

# Create your models here.
from core.models import Domecile


class Campaign(models.Model):
    parent_campaign = models.ForeignKey('Campaign', null=True)
    name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)

    @staticmethod
    def get_latest_top_level_campaign():
        return Campaign.objects.filter(parent_campaign__isnull=True).order_by('date_added').first()


class DownloadFile(models.Model):
    parent_campaign = models.ForeignKey(Campaign)
    short_name = models.CharField(max_length=100)
    description = models.TextField()
    download_path = models.FileField()


