__author__ = 'scotm'
from django.conf.urls import patterns, url

from views import WardView, WardListView


urlpatterns = patterns('',
                       url(r'^(?P<pk>[0-9]+)', WardView.as_view(), name='ward_view'),
                       url(r'^', WardListView.as_view(), name='ward_list'),
)
