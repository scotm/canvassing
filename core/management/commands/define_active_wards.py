from __future__ import print_function

__author__ = 'scotm'

from django.core.management import BaseCommand

from core.models import Ward, Contact


class Command(BaseCommand):
    help = "Makes wards active if they've got contacts in them"

    def handle(self, *args, **options):
        for i in Ward.objects.all():
            i.active = False
            if Contact.objects.filter(domecile__postcode_point__point__within=i.geom).exists():
                i.active = True
            if i.active:
                print("%s is active" % unicode(i))
            i.save(update_fields=['active'])
