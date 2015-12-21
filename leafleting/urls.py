from django.conf.urls import url
from django.views.generic import TemplateView

from core.models import Ward, Region
from leafleting.models import LeafletRun, CanvassRun
from leafleting.views import LeafletRunCreate, LeafletHomepage, CanvassHomepage, RunDetailView, \
    CanvassRunListView, LeafletRunListView, RunPicker, AreaPicker, PrintRunDetailView, CanvassRunDelete, CanvassRunBook, \
    CanvassRunUnbook, UserCanvassRunFind, CanvassPicker, DataInput, DataInputJSONAcceptor, canvass_run_create, \
    domecile_map_view, domecile_address_view

__author__ = 'scotm'

urlpatterns = [
    url(r'^leafleting/why_leaflet/$', TemplateView.as_view(template_name='why_leaflet.html'), name='why_leaflet'),
    url(r'^leafleting/leaflet_run_create', LeafletRunCreate.as_view(), name='leaflet_run_create'),
    url(r'^leafleting/region/(?P<pk>[0-9]+)', RunPicker.as_view(template_name='leafleting_picker.html', model=Region),
        name='leaflet_region_view'),
    url(r'^leafleting/ward/(?P<pk>[0-9]+)', RunPicker.as_view(model=Ward, template_name='leafleting_picker.html'),
        name='leaflet_ward_view'),
    url(r'^leafleting/ward/$', AreaPicker.as_view(model=Ward, template_name='leafleting_ward_picker.html'),
        name='leaflet_ward_list'),
    url(r'^leafleting/run/(?P<pk>[0-9]+)$', RunDetailView.as_view(model=LeafletRun), name='leaflet_run'),
    url(r'^leafleting/list/', LeafletRunListView.as_view(), name='leaflet_list'),
    url(r'^leafleting/$', LeafletHomepage.as_view(), name='leaflet_homepage'),

    url(r'^canvassing/why_canvass/$', TemplateView.as_view(template_name="why_canvass.html"), name='why_canvass'),
    url(r'^canvassing/canvass_run_create', canvass_run_create, name='canvass_run_create'),
    url(r'^canvassing/region/(?P<pk>[0-9]+)', CanvassPicker.as_view(model=Region), name='canvass_region_view'),
    url(r'^canvassing/region/$', AreaPicker.as_view(template_name='canvassing_region_picker.html', model=Region),
        name='canvass_region_list'),
    url(r'^canvassing/ward/(?P<pk>[0-9]+)', CanvassPicker.as_view(model=Ward), name='canvass_ward_view'),
    url(r'^canvassing/ward/$', AreaPicker.as_view(template_name='canvassing_ward_picker.html', model=Ward),
        name='canvass_ward_list'),

    url(r'^canvassing/run/input/(?P<pk>[0-9]+)$', DataInput.as_view(model=CanvassRun), name='canvass_run_input'),
    url(r'^canvassing/run/input/ajax', DataInputJSONAcceptor.as_view(), name='canvass_run_input_ajax'),
    url(r'^canvassing/run/print/(?P<pk>[0-9]+)$', PrintRunDetailView.as_view(model=CanvassRun),
        name='canvass_run_print'),
    url(r'^canvassing/run/unbook/(?P<pk>[0-9]+)$', CanvassRunUnbook.as_view(), name='canvass_run_unbook'),
    url(r'^canvassing/run/book/(?P<pk>[0-9]+)$', CanvassRunBook.as_view(), name='canvass_run_book'),
    url(r'^canvassing/run/delete/(?P<pk>[0-9]+)$', CanvassRunDelete.as_view(), name='canvass_run_delete'),
    url(r'^canvassing/run/(?P<pk>[0-9]+)$', RunDetailView.as_view(model=CanvassRun), name='canvass_run'),
    url(r'^canvassing/booked/$', UserCanvassRunFind.as_view(), name='booked_lists'),
    url(r'^canvassing/list/', CanvassRunListView.as_view(), name='canvass_list'),
    url(r'^canvassing/$', CanvassHomepage.as_view(), name='canvass_homepage'),
    url(r'^ajax/get_domeciles$', domecile_map_view, name='get_domeciles'),
    url(r'^ajax/get_addresses$', domecile_address_view, name='get_addresses'),
]
