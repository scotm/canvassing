from __future__ import print_function

__author__ = 'scotm'

from django.core.management import BaseCommand

from core.models import Region

class Command(BaseCommand):
    help = 'Fills up the DB with regional data'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=unicode)

    def handle(self, *args, **options):
        for filename in options['filename']:
            Region.fill_up_db(filename, verbose=True)

        Region.clean_up()
