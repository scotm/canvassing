from django.views.generic import TemplateView
from core.models import Ward, Region
from leafleting.models import LeafletRun, CanvassRun

__author__ = 'scotm'
from django.conf.urls import patterns, url

from leafleting.views import LeafletRunCreate, CanvassRunCreate, LeafletHomepage, CanvassHomepage, RunDetailView, \
    CanvassRunListView, LeafletRunListView, RunPicker, AreaPicker


urlpatterns = patterns('',
                       url(r'^leafleting/why_leaflet/$', TemplateView.as_view(template_name='why_leaflet.html'), name='why_leaflet'),
                       url(r'^leafleting/leaflet_run_create', LeafletRunCreate.as_view(), name='leaflet_run_create'),
                       url(r'^leafleting/region/(?P<pk>[0-9]+)', RunPicker.as_view(template_name='leafleting_picker.html', model=Region), name='leaflet_region_view'),
                       url(r'^leafleting/ward/(?P<pk>[0-9]+)', RunPicker.as_view(model=Ward,template_name='leafleting_picker.html'), name='leaflet_ward_view'),
                       url(r'^leafleting/ward/$', AreaPicker.as_view(model=Ward, template_name='leafleting_ward_picker.html'), name='leaflet_ward_list'),
                       url(r'^leafleting/run/(?P<pk>[0-9]+)$', RunDetailView.as_view(model=LeafletRun), name='leaflet_run'),
                       url(r'^leafleting/list/', LeafletRunListView.as_view(), name='leaflet_list'),
                       url(r'^leafleting/$', LeafletHomepage.as_view(), name='leaflet_homepage'),

                       url(r'^canvassing/why_canvass/$', TemplateView.as_view(template_name="why_canvass.html"), name='why_canvass'),
                       url(r'^canvassing/canvass_run_create', CanvassRunCreate.as_view(), name='canvass_run_create'),
                       url(r'^canvassing/region/(?P<pk>[0-9]+)', RunPicker.as_view(template_name='canvassing_picker.html', model=Region), name='canvass_region_view'),
                       url(r'^canvassing/ward/(?P<pk>[0-9]+)', RunPicker.as_view(template_name='canvassing_picker.html', model=Ward), name='canvass_ward_view'),
                       url(r'^canvassing/ward/$', AreaPicker.as_view(template_name='canvassing_ward_picker.html', model=Ward), name='canvass_ward_list'),
                       url(r'^canvassing/run/(?P<pk>[0-9]+)$', RunDetailView.as_view(model=CanvassRun), name='canvass_run'),
                       url(r'^canvassing/list/', CanvassRunListView.as_view(), name='canvass_list'),
                       url(r'^canvassing/$', CanvassHomepage.as_view(), name='canvass_homepage'),
                       )
