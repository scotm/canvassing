from __future__ import print_function
__author__ = 'scotm'
import bz2
from subprocess import call

import os
from datetime import datetime
import dropbox
from django.conf import settings
from django.core.management.base import BaseCommand
from ssp_canvassing.settings.secrets import DROPBOX_ACCESS_TOKEN


class Command(BaseCommand):
    help = "Dumps DB to Drobox"

    def handle(self, *args, **options):
        client = dropbox.client.DropboxClient(DROPBOX_ACCESS_TOKEN)
        now = datetime.now().strftime('%Y-%m-%d')
        db_name = settings.DATABASES['default']['NAME']
        filename = 'canvassing_db_%s.pgsql' % now
        with open(filename, 'wb') as myfile:
            call(["pg_dump", "-T", "planet*", db_name], stdout=myfile)
        print("Dump complete - compressing.")
        call(["bzip2", filename])
        filename += ".bz2"
        print("Database successfully dumped. Uploading to Dropbox.")
        with open(filename) as myfile:
            try:
                client.file_create_folder(now)
                print("Creating folder")
            except dropbox.rest.ErrorResponse as e:
                if e.status != 403:
                    raise
            print("Uploading backup file: %s ..." % filename)
            response = client.put_file("%s" % (filename), myfile)
            print(" done. %s" % response['size'])
        os.unlink(filename)