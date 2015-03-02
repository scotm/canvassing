from __future__ import print_function
# Create your views here.
from django.views.generic import DetailView, ListView
from json_views.views import JSONDataView

from core.models import Ward
from leafleting.models import LeafletRun
from postcode_locator.models import PostcodeMapping


class WardListView(ListView):
    model = Ward
    template_name = 'leafleting/ward_list.html'

    def get_queryset(self):
        return super(WardListView, self).get_queryset()


class WardView(DetailView):
    model = Ward
    template_name = 'leafleting/ward_view.html'


class LeafletRunCreate(JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(LeafletRunCreate, self).get_context_data(**kwargs)
        l = LeafletRun.objects.create(**{'name':self.request.GET['run_name'], 'notes':self.request.GET['run_notes']})
        for x in self.request.GET.getlist('selected_postcodes[]'):
            l.postcode_points.add(PostcodeMapping.match_postcode(x))
        l.save()
        context.update({'outcome':'success'})
        return context

