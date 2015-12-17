from braces.views import LoginRequiredMixin
from braces.views._access import AccessMixin
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView
from json_views.views import JSONDataView

from core.models import Contact, Domecile, Ward, Region


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() or settings.ALL_ALLOWED:
            return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        return self.handle_no_permission(request)


class ContactView(LoginRequiredMixin, DetailView):
    model = Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    paginate_by = 100


def domecile_map_view(request):
    if 'region' in request.GET:
        klass = Region
        area = request.GET['region']
    elif 'ward' in request.GET:
        klass = Ward
        area = request.GET['ward']
    else:
        return JsonResponse(data={})
    bbox = request.GET['BBox'].split(',')
    query_type = request.GET['query_type']
    queryset = Domecile.get_postcode_points(southwest=(bbox[0], bbox[1]), northeast=(bbox[2], bbox[3]),
                                            region=klass.objects.get(pk=int(area)), query_type=query_type)

    data = [{'postcode': x.postcode, 'point': x.postcode_point.point} for x in queryset]
    for i in data:
        i['point'][0] = round(i['point'][0], 7)
        i['point'][1] = round(i['point'][1], 7)
    return JsonResponse(data={'data': data})


class DomecileMapView(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(DomecileMapView, self).get_context_data(**kwargs)
        if 'region' in self.request.GET:
            klass = Region
            area = self.request.GET['region']
        elif 'ward' in self.request.GET:
            klass = Ward
            area = self.request.GET['ward']
        else:
            return context
        bbox = self.request.GET['BBox'].split(',')
        query_type = self.request.GET['query_type']
        queryset = Domecile.get_postcode_points(southwest=(bbox[0], bbox[1]), northeast=(bbox[2], bbox[3]),
                                                region=klass.objects.get(pk=int(area)), query_type=query_type)

        data = [{'postcode': x.postcode, 'point': x.postcode_point.point} for x in queryset]
        for i in data:
            i['point'][0] = round(i['point'][0], 7)
            i['point'][1] = round(i['point'][1], 7)
        context.update({'data': data})
        return context


class DomecileAddressView(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        from postcode_locator.models import PostcodeMapping
        context = super(DomecileAddressView, self).get_context_data(**kwargs)
        try:
            postcode = self.request.GET['postcode']
        except:
            return context
        try:
            data = Domecile.get_sorted_addresses(postcode)
            summary = Domecile.get_summary_of_postcode(postcode)
            contacts_count = Contact.objects.filter(
                    domecile__postcode_point=PostcodeMapping.match_postcode(postcode)).count()
            context.update({'data': data, 'postcode': postcode, 'summary': summary[0], 'buildings': summary[1],
                            'contacts': contacts_count})
        except:
            context.update(
                    {'data': None, 'postcode': postcode, 'summary': 'No data found', 'buildings': 0, 'contacts': 0})
        return context


class HomepageView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        from campaigns.models import Campaign

        kwargs.update({'current_campaign': Campaign.get_latest_top_level_campaign()})
        return super(HomepageView, self).get_context_data(**kwargs)


class LoginTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'why_canvass.html'
