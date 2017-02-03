from __future__ import print_function
from django.db.models.loading import get_model
from django.core.management import BaseCommand
from core.models import Contact
__author__ = 'scotm'


def make_active(klasses):
    for klass in klasses:
        klass = get_model("core", klass)
        for i in klass.objects.all():
            i.active = False
            if Contact.objects.filter(domecile__postcode_point__point__within=i.geom).exists():
                i.active = True
            if i.active:
                print(u"{} is active".format(i))
            i.save(update_fields=['active'])


class Command(BaseCommand):
    help = "Makes wards active if they've got contacts in them"

    klasses = ['Ward', 'Region']

    def handle(self, *args, **options):
        make_active(self.klasses)
