from campaigns.views import FindContactList, SignPetition

__author__ = 'scotm'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^signatures/$', FindContactList.as_view(), name='find_contact'),
                       url(r'^signatures/ajax_sign$', SignPetition.as_view(), name='sign_petition_ajax'),
)
