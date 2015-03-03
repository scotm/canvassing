from __future__ import print_function
# Create your views here.
from django.views.generic import ListView
from json_views.views import JSONDataView

from leafleting.models import LeafletRun, CanvassRun
from postcode_locator.models import PostcodeMapping

class LeafletRunCreate(JSONDataView):
    model = LeafletRun
    def get_context_data(self, **kwargs):
        context = super(LeafletRunCreate, self).get_context_data(**kwargs)
        postcodes = self.request.GET.getlist('selected_postcodes[]')
        if not postcodes:
            raise Exception("A list of postcodes is required.")

        leaflet_run = self.model.objects.create(**{'name':self.request.GET['run_name'], 'notes':self.request.GET['run_notes']})
        for x in postcodes:
            leaflet_run.postcode_points.add(PostcodeMapping.match_postcode(x))
        leaflet_run.save()
        context.update({'outcome':'success'})
        return context

class LeafletRunListView(ListView):
    model = LeafletRun

class CanvassRunCreate(LeafletRunCreate):
    model = CanvassRun

class CanvassRunListView(ListView):
    model = CanvassRun
