from django.contrib import admin

from models import ElectoralRegistrationOffice, Contact, Domecile


class DomecileAdmin(admin.ModelAdmin):
    list_display = ('obj_name', 'postcode')
    fields = (
        "address_1", "address_2", "address_3", "address_4", "address_5", "address_6", "address_7", "address_8",
        "address_9", "phone_number", "postcode"
    )

    def obj_name(self, obj):
        return "%s" % unicode(obj)

    obj_name.short_description = 'Name'

# Register your models here.

admin.site.register(Domecile, DomecileAdmin)
admin.site.register(ElectoralRegistrationOffice)
admin.site.register(Contact)