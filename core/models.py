from django.contrib.gis.db import models
from django.core.validators import RegexValidator


class Campaign(models.Model):
    parent_campaign = models.ForeignKey('Campaign', null=True)
    name = models.CharField(max_length=100)


class DownloadFile(models.Model):
    parent_campaign = models.ForeignKey(Campaign)
    short_name = models.CharField(max_length=100)
    description = models.TextField()
    download_path = models.FileField()


class ElectoralRegistrationOffice(models.Model):
    name = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    address_3 = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True)


class Domecile(models.Model):
    electoral_registration_office = models.ForeignKey(ElectoralRegistrationOffice)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    address_3 = models.CharField(max_length=100)
    address_4 = models.CharField(max_length=500)
    address_5 = models.CharField(max_length=60)
    address_6 = models.CharField(max_length=60)
    address_7 = models.CharField(max_length=60)
    address_8 = models.CharField(max_length=60)
    address_9 = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=10)
    postcode_point = models.PointField()

    objects = models.GeoManager()

    def __unicode__(self):
        return ", ".join([getattr(self, x) for x in
                          ["address_1", "address_2", "address_3", "address_4", "address_5", "address_6", "address_7",
                           "address_8", "address_9", "postcode"]])


class Contact(models.Model):
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)
    surname = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10)
    domecile = models.ForeignKey(Domecile)
    opt_out = models.BooleanField(default=False)

    def __unicode__(self):
        return " ".join([getattr(self, x) for x in ["first_name", "initials", "surname", "suffix"]])


class Conversation(models.Model):
    person = models.ForeignKey(Contact)
    notes = models.TextField()


class LeafletDrop(models.Model):
    leaflet = models.ForeignKey(DownloadFile)
    households = models.ManyToManyField(Domecile)
