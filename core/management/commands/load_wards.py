from __future__ import print_function

__author__ = 'scotm'

from django.core.management import BaseCommand

from core.models import Ward


class Command(BaseCommand):
    help = 'Fills up the DB with regional data'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=unicode)

    def handle(self, *args, **options):
        print(args, options)
        for filename in args:
            Ward.fill_up_db(filename, verbose=True)
