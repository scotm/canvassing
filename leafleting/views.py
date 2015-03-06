from __future__ import print_function
# Create your views here.
from braces.views import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from json_views.views import JSONDataView
from core.models import Ward

from leafleting.models import LeafletRun, CanvassRun
from postcode_locator.models import PostcodeMapping


class LeafletRunCreate(LoginRequiredMixin, JSONDataView):
    model = LeafletRun

    def get_context_data(self, **kwargs):
        context = super(LeafletRunCreate, self).get_context_data(**kwargs)
        postcodes = self.request.GET.getlist('selected_postcodes[]')
        if not postcodes:
            raise Exception("A list of postcodes is required.")

        leaflet_run = self.model.objects.create(
            **{'name': self.request.GET['run_name'], 'notes': self.request.GET['run_notes']})
        for x in postcodes:
            leaflet_run.postcode_points.add(PostcodeMapping.match_postcode(x))
        leaflet_run.save()
        context.update({'outcome': 'success'})
        return context


class CanvassRunCreate(LeafletRunCreate):
    model = CanvassRun


# TODO: Unusable
class LeafletRunEdit(LoginRequiredMixin, JSONDataView):
    model = LeafletRun

    def get_context_data(self, **kwargs):
        return super(LeafletRunEdit, self).get_context_data(**kwargs)


class LeafletHomepage(LoginRequiredMixin, TemplateView):
    run_klass = LeafletRun
    template_name = 'leafleting_homepage.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'runs': self.run_klass.objects.all()[:5]})
        return super(LeafletHomepage, self).get_context_data(**kwargs)


class CanvassHomepage(LeafletHomepage):
    run_klass = CanvassRun
    template_name = 'canvassing_homepage.html'


class LeafletRunListView(LoginRequiredMixin, ListView):
    model = LeafletRun


class CanvassRunListView(LoginRequiredMixin, ListView):
    model = CanvassRun


class LeafletingPicker(LoginRequiredMixin, DetailView):
    model = Ward
    template_name = 'leafleting_picker.html'


class CanvassingPicker(LeafletingPicker):
    template_name = 'canvassing_picker.html'


class LeafletWardPicker(LoginRequiredMixin, ListView):
    model = Ward
    template_name = 'leafleting_ward_picker.html'


class CanvassWardPicker(LeafletWardPicker):
    template_name = 'canvassing_ward_picker.html'
