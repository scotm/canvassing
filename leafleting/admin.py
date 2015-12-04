from django.contrib import admin
from leafleting.models import LeafletRun, CanvassRun


class CanvassRunAdmin(admin.ModelAdmin):
    exclude = ('postcode_points','ward','intermediate_zone','datazone',)
    fields = ('name', 'notes', 'created_by', 'date_available', 'questionaire')


# Register your models here.
admin.site.register(LeafletRun)
admin.site.register(CanvassRun)
