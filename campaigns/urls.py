from campaigns.views import FindContactList

__author__ = 'scotm'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^signatures/$', FindContactList.as_view(), name='find_contact'),
)
