from django.contrib.gis.db import models


class BaseOsmModel(models.Model):
    access = models.TextField(blank=True)
    addr_housename = models.TextField(db_column='addr:housename', blank=True)
    addr_housenumber = models.TextField(db_column='addr:housenumber', blank=True)
    addr_interpolation = models.TextField(db_column='addr:interpolation', blank=True)
    admin_level = models.TextField(blank=True)
    aerialway = models.TextField(blank=True)
    aeroway = models.TextField(blank=True)
    amenity = models.TextField(blank=True)
    area = models.TextField(blank=True)
    barrier = models.TextField(blank=True)
    bicycle = models.TextField(blank=True)
    boundary = models.TextField(blank=True)
    brand = models.TextField(blank=True)
    bridge = models.TextField(blank=True)
    building = models.TextField(blank=True)
    construction = models.TextField(blank=True)
    covered = models.TextField(blank=True)
    culvert = models.TextField(blank=True)
    cutting = models.TextField(blank=True)
    denomination = models.TextField(blank=True)
    disused = models.TextField(blank=True)
    embankment = models.TextField(blank=True)
    foot = models.TextField(blank=True)
    generator_source = models.TextField(db_column='generator:source', blank=True)
    harbour = models.TextField(blank=True)
    highway = models.TextField(blank=True)
    historic = models.TextField(blank=True)
    horse = models.TextField(blank=True)
    intermittent = models.TextField(blank=True)
    junction = models.TextField(blank=True)
    landuse = models.TextField(blank=True)
    layer = models.TextField(blank=True)
    leisure = models.TextField(blank=True)
    lock = models.TextField(blank=True)
    man_made = models.TextField(blank=True)
    military = models.TextField(blank=True)
    motorcar = models.TextField(blank=True)
    name = models.TextField(blank=True)
    natural = models.TextField(blank=True)
    office = models.TextField(blank=True)
    oneway = models.TextField(blank=True)
    operator = models.TextField(blank=True)
    place = models.TextField(blank=True)
    population = models.TextField(blank=True)
    power = models.TextField(blank=True)
    power_source = models.TextField(blank=True)
    public_transport = models.TextField(blank=True)
    railway = models.TextField(blank=True)
    ref = models.TextField(blank=True)
    religion = models.TextField(blank=True)
    route = models.TextField(blank=True)
    service = models.TextField(blank=True)
    shop = models.TextField(blank=True)
    sport = models.TextField(blank=True)
    surface = models.TextField(blank=True)
    toll = models.TextField(blank=True)
    tourism = models.TextField(blank=True)
    tower_type = models.TextField(db_column='tower:type', blank=True)
    tunnel = models.TextField(blank=True)
    water = models.TextField(blank=True)
    waterway = models.TextField(blank=True)
    wetland = models.TextField(blank=True)
    width = models.TextField(blank=True)
    wood = models.TextField(blank=True)
    z_order = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


# Create your models here.
class PlanetOsmLine(BaseOsmModel):
    osm_id = models.BigIntegerField(blank=True, primary_key=True)
    way_area = models.FloatField(blank=True, null=True)
    way = models.LineStringField(srid=900913, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'planet_osm_line'


class PlanetOsmPoint(BaseOsmModel):
    osm_id = models.BigIntegerField(blank=True, primary_key=True)
    capital = models.TextField(blank=True)
    ele = models.TextField(blank=True)
    poi = models.TextField(blank=True)
    way = models.PointField(srid=900913, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'planet_osm_point'


class PlanetOsmPolygon(BaseOsmModel):
    osm_id = models.BigIntegerField(blank=True, primary_key=True)
    tracktype = models.TextField(blank=True)
    way_area = models.FloatField(blank=True, null=True)
    way = models.GeometryField(srid=900913, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'planet_osm_polygon'


class PlanetOsmRoads(BaseOsmModel):
    osm_id = models.BigIntegerField(blank=True, primary_key=True)
    tracktype = models.TextField(blank=True)
    way_area = models.FloatField(blank=True, null=True)
    way = models.LineStringField(srid=900913, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'planet_osm_roads'
