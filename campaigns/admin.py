from django.contrib import admin

# Register your models here.
from campaigns.models import Campaign, DownloadFile, AssignedLeafletRun, PrintableCanvassingRun, Signature

admin.site.register(Campaign)
admin.site.register(DownloadFile)
admin.site.register(AssignedLeafletRun)
admin.site.register(PrintableCanvassingRun)
admin.site.register(Signature)
