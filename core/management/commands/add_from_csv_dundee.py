__author__ = 'scotm'
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Fills up the DB with elector data'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=unicode)

    def handle(self, *args, **options):
        print options, args
        filename = args[0]
