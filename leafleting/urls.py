__author__ = 'scotm'
from django.conf.urls import patterns, url

from views import LeafletRunCreate
from core.views import WardListView, WardView


urlpatterns = patterns('',
                       url(r'^leafleting/leaflet_run_create', LeafletRunCreate.as_view(), name='leaflet_run_create'),
                       url(r'^leafleting/ward/(?P<pk>[0-9]+)', WardView.as_view(), name='ward_view'),
                       url(r'^leafleting/ward/$', WardListView.as_view(), name='ward_list'),
                       url(r'^canvassing/canvass_run_create', LeafletRunCreate.as_view(), name='canvass_run_create'),
                       url(r'^canvassing/ward/(?P<pk>[0-9]+)', WardView.as_view(), name='canvass_ward_view'),
                       url(r'^canvassing/ward/$', WardListView.as_view(), name='canvass_ward_list'),
)
