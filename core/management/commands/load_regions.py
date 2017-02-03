from __future__ import print_function
from django.core.management import BaseCommand
from core.models import Region

__author__ = 'scotm'


class Command(BaseCommand):
    help = 'Fills up the DB with regional data'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=unicode)

    def handle(self, *args, **options):
        for filename in options['filename']:
            Region.fill_up_db(filename, verbose=True)

        clean_up()


def clean_up(DEBUG=False):
    import gc
    from random import shuffle
    from postcode_locator.models import PostcodeMapping

    # We're only interested in Scottish constituencies - so delete the rest - their code begins with an "S".
    Region.objects.exclude(code__startswith="S").delete()

    # The Highlands and Islands electoral region is a massive pain in the arse.
    # Many, many pieces, small islands and areas - hardly any of them usable.
    print("Cleaning up the Highlands and Islands electoral region")
    highlands_regions = Region.objects.filter(name='Highlands and Islands')

    if PostcodeMapping.objects.all().count() > 0:
        # Prune out the over two thousand landmasses without postcode points.
        no_postcode_pks = [region.pk for region in highlands_regions if
                           not PostcodeMapping.objects.filter(point__within=region.geom).exists()]
        Region.objects.filter(pk__in=no_postcode_pks).delete()
        print("Deleted those without postcodes")

    # Now we make a union of all the remaining geometry.
    print("Unifying Highlands & Islands geometry...")
    highlands = Region.objects.filter(name='Highlands and Islands').values_list('geom', flat=True)
    highlands = sorted(highlands, key=lambda x: len(x[0][0]), reverse=True)  # Sort them, so we can pop the top off
    keep_separate = highlands.pop(0)  # This one is huge, and will slow down processing. Unify it at the end.
    shuffle(highlands)

    # Process pairs of geometry, join them together and repeat until there's one left.
    while True:
        if DEBUG:
            print(len(highlands))
        new_highlands = []
        while highlands:
            if len(highlands) == 0:
                break
            if len(highlands) == 1:  # If there's only one left, just add it to the next run
                new_highlands += highlands.pop()
                break
            geom1, geom2 = highlands.pop(), highlands.pop()
            new_highlands.append(geom1.union(geom2))
        highlands = new_highlands
        gc.collect()
        if len(highlands) == 1:  # If there's only one left, we're done.
            break

    highlands = highlands[0].union(keep_separate)  # Now join the huge one to the unified pieces.
    print("done")

    # Simplify the region. 0.0005 seems a decent simplification factor: higher removes more points from the geom
    print("Simplifying the geometry a little, for ease of future computation")
    simplified_highlands = highlands.simplify(0.0005, preserve_topology=True)

    # And save it.
    r = Region(name='Highlands and Islands SIMPLIFIED', description='Scottish Parliament Electoral Region',
               hectares='4050000', geom=simplified_highlands, number=0.0, number0=0.0, polygon_id=0.0, unit_id=0.0,
               code='S', area=0.0, type_code='', descript0='', type_cod0='', descript1='')
    r.save()

    # Nuke the residue - We've already got a decent geom of it.
    Region.objects.filter(name='Highlands and Islands').delete()
