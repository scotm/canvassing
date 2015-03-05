from django.views.generic import TemplateView

__author__ = 'scotm'
from django.conf.urls import patterns, url

from leafleting.views import LeafletingPicker, LeafletWardPicker, LeafletRunCreate, CanvassRunCreate, CanvassingPicker, \
    CanvassWardPicker, LeafletHomepage, CanvassHomepage
from core.views import LoginTemplateView


urlpatterns = patterns('',
                       url(r'^leafleting/why_leaflet/$', TemplateView.as_view(template_name='why_leaflet.html'), name='why_leaflet'),
                       url(r'^leafleting/leaflet_run_create', LeafletRunCreate.as_view(), name='leaflet_run_create'),
                       url(r'^leafleting/ward/(?P<pk>[0-9]+)', LeafletingPicker.as_view(), name='ward_view'),
                       url(r'^leafleting/ward/$', LeafletWardPicker.as_view(), name='leaflet_ward_list'),
                       url(r'^leafleting/$', LeafletHomepage.as_view(), name='leaflet_homepage'),

                       url(r'^canvassing/why_canvass/$', TemplateView.as_view(), name='why_canvass'),
                       url(r'^canvassing/canvass_run_create', CanvassRunCreate.as_view(), name='canvass_run_create'),
                       url(r'^canvassing/ward/(?P<pk>[0-9]+)', CanvassingPicker.as_view(), name='canvass_ward_view'),
                       url(r'^canvassing/ward/$', CanvassWardPicker.as_view(), name='canvass_ward_list'),
                       url(r'^canvassing/$', CanvassHomepage.as_view(), name='canvass_homepage'),
)
