from django.contrib import admin

# Register your models here.
from campaigns.models import Campaign, DownloadFilei

admin.site.register(Campaign)
admin.site.register(DownloadFile)