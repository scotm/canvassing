from django.conf.urls import url

from campaigns.views import FindContactList, SignPetition, GetPetition, sign_petition_view

__author__ = 'scotm'

urlpatterns = [
    url(r'^signatures/$', FindContactList.as_view(), name='find_contact'),
    url(r'^signatures/get_signature$', GetPetition.as_view(), name='get_petition_ajax'),
    url(r'^signatures/ajax_sign$', sign_petition_view, name='sign_petition_ajax'),
]
