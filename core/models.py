from django.db import models

from postcode_locator.models import PostcodeMapping


class ElectoralRegistrationOffice(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    address_3 = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True)

    def __unicode__(self):
        return self.name


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
    postcode_point = models.ForeignKey(PostcodeMapping)

    def __unicode__(self):
        return ", ".join(getattr(self, x) for x in
                         ["address_1", "address_2", "address_3", "address_4", "address_5", "address_6", "address_7",
                          "address_8", "address_9", "postcode"] if getattr(self, x))

    def save(self, *args, **kwargs):
        self.postcode_point = PostcodeMapping.match_postcode(self.postcode, raise_exceptions=False)
        super(Domecile, self).save(*args, **kwargs)


class Contact(models.Model):
    ero_number = models.IntegerField()
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)
    surname = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10)
    domecile = models.ForeignKey(Domecile)
    opt_out = models.BooleanField(default=False)

    def __unicode__(self):
        return " ".join([getattr(self, x) for x in ["first_name", "initials", "surname", "suffix"] if getattr(self,x)])


class Conversation(models.Model):
    person = models.ForeignKey(Contact)
    notes = models.TextField()
