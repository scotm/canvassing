from django.contrib import admin

# Register your models here.
from campaigns.models import Campaign, DownloadFile, Signature

admin.site.register(Campaign)
admin.site.register(DownloadFile)
admin.site.register(Signature)
