from django.contrib.gis import admin
from core.models import ElectoralRegistrationOffice, Contact, Domecile, Ward, Region, PoliticalParty, \
    IntermediateZone, DataZone


class DomecileAdmin(admin.ModelAdmin):
    list_display = ('obj_name', 'postcode')
    fields = (
        "address_1", "address_2", "address_3", "address_4", "address_5", "address_6", "address_7", "address_8",
        "address_9", "phone_number", "postcode"
    )

    def obj_name(self, obj):
        return "%s" % unicode(obj)

    obj_name.short_description = 'Name'


class myOSMGeoAdmin(admin.OSMGeoAdmin):
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'


class WardAdmin(myOSMGeoAdmin):
    search_fields = ['ward_name']
    list_filter = ['local_authority_name', 'active']

    def get_queryset(self, request):
        return super(WardAdmin, self).get_queryset(request).defer('geom')


class RegionAdmin(myOSMGeoAdmin):
    search_fields = ['name']
    list_filter = ['description', 'active']

    def get_queryset(self, request):
        return super(RegionAdmin, self).get_queryset(request).defer('geom')


class IntermediateZoneAdmin(myOSMGeoAdmin):
    search_fields = ['name']
    list_filter = ['local_authority_name', 'active']

    def get_queryset(self, request):
        return super(IntermediateZoneAdmin, self).get_queryset(request).defer('geom')


class DataZoneAdmin(myOSMGeoAdmin):
    search_fields = ['name']
    list_filter = ['councila_2']

    def get_queryset(self, request):
        return super(DataZoneAdmin, self).get_queryset(request).defer('geom')

# Register your models here.
admin.site.register(PoliticalParty)
admin.site.register(Domecile, DomecileAdmin)
admin.site.register(ElectoralRegistrationOffice)
admin.site.register(Contact)
admin.site.register(Region, RegionAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(IntermediateZone, IntermediateZoneAdmin)
admin.site.register(DataZone, DataZoneAdmin)
