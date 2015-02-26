from django.views.generic import DetailView, ListView
from json_views.views import JSONDataView

from core.models import Contact, Domecile, Ward


class ContactView(DetailView):
    model = Contact


class ContactListView(ListView):
    model = Contact


class DomecileMapView(JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(DomecileMapView, self).get_context_data(**kwargs)
        region = self.request.GET['region']
        bbox = self.request.GET['BBox'].split(',')
        queryset = Domecile.get_postcode_points(southwest=(bbox[0], bbox[1]), northeast=(bbox[2], bbox[3]),
                                                region=Ward.objects.get(pk=int(region)))
        data = [{'postcode':x.postcode, 'point':x.postcode_point.point} for x in queryset]
        context.update({'data':data})
        return context
