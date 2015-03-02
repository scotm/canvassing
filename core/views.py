from functools import cmp_to_key

from django.views.generic import DetailView, ListView
from json_views.views import JSONDataView

from core.models import Contact, Domecile, Ward


class ContactView(DetailView):
    model = Contact


class ContactListView(ListView):
    model = Contact
    paginate_by = 100


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

def consume_int(x):
    sum_total = 0
    for i in x:
        if i.isdigit():
            sum_total = sum_total*10 + int(i)
        else:
            break
    return sum_total

def domecile_cmp(x,y):
    if x.address_4 != y.address_4:
        return cmp(x.address_4, y.address_4)
    a, b = consume_int(x.address_2),consume_int(y.address_2)
    if a == b:
        return cmp(x.address_2, y.address_2)
    return cmp(a, b)

class DomecileAddressView(JSONDataView):
    def get_context_data(self, **kwargs):
        from django.db.models import Count
        context = super(DomecileAddressView, self).get_context_data(**kwargs)
        postcode = self.request.GET['postcode']
        queryset = Domecile.objects.filter(postcode=postcode).annotate(num_contacts=Count('contact'))
        data = [unicode(y)+" (%d)" % y.num_contacts for y in sorted(queryset, key=cmp_to_key(domecile_cmp))]
        context.update({'data':data, 'postcode':postcode})
        return context

