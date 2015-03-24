from django.views.generic import TemplateView

__author__ = 'scotm'
from django.conf.urls import patterns, url

from leafleting.views import LeafletingPicker, LeafletWardPicker, LeafletRunCreate, CanvassRunCreate, \
    LeafletHomepage, CanvassHomepage, CanvassRunDetailView, LeafletRunDetailView, CanvassRunListView, LeafletRunListView, RegionLeafletingPicker


urlpatterns = patterns('',
                       url(r'^leafleting/why_leaflet/$', TemplateView.as_view(template_name='why_leaflet.html'),
                           name='why_leaflet'),
                       url(r'^leafleting/leaflet_run_create', LeafletRunCreate.as_view(), name='leaflet_run_create'),
                       url(r'^leafleting/ward/(?P<pk>[0-9]+)', LeafletingPicker.as_view(), name='leaflet_ward_view'),
                       url(r'^leafleting/ward/$', LeafletWardPicker.as_view(), name='leaflet_ward_list'),
                       url(r'^leafleting/run/(?P<pk>[0-9]+)$', LeafletRunDetailView.as_view(), name='leaflet_run'),
                       url(r'^leafleting/list/', LeafletRunListView.as_view(), name='leaflet_list'),
                       url(r'^leafleting/$', LeafletHomepage.as_view(), name='leaflet_homepage'),

                       url(r'^canvassing/why_canvass/$', TemplateView.as_view(template_name="why_canvass.html"),
                           name='why_canvass'),
                       url(r'^canvassing/canvass_run_create', CanvassRunCreate.as_view(), name='canvass_run_create'),
                       url(r'^canvassing/region/(?P<pk>[0-9]+)',
                           RegionLeafletingPicker.as_view(template_name='canvassing_picker.html'), name='canvass_region_view'),
                       url(r'^canvassing/ward/(?P<pk>[0-9]+)',
                           LeafletingPicker.as_view(template_name='canvassing_picker.html'), name='canvass_ward_view'),
                       url(r'^canvassing/ward/$',
                           LeafletWardPicker.as_view(template_name='canvassing_ward_picker.html'),
                           name='canvass_ward_list'),
                       url(r'^canvassing/run/(?P<pk>[0-9]+)$', CanvassRunDetailView.as_view(), name='canvass_run'),
                       url(r'^canvassing/list/', CanvassRunListView.as_view(), name='canvass_list'),
                       url(r'^canvassing/$', CanvassHomepage.as_view(), name='canvass_homepage'),
                       )
