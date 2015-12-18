from braces.views import LoginRequiredMixin
from braces.views._access import AccessMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

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


@login_required
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
    data = Domecile.get_postcode_points(southwest=(bbox[0], bbox[1]), northeast=(bbox[2], bbox[3]),
                                        region=klass.objects.get(pk=int(area)), query_type=query_type)
    for i in data:
        i['point'][0] = round(i['point'][0], 6)
        i['point'][1] = round(i['point'][1], 6)
    return JsonResponse(data={'data': data})


@login_required
def domecile_address_view(request):
    from postcode_locator.models import PostcodeMapping
    if not request.GET.get('postcode', None):
        return JsonResponse(data={})
    try:
        summary = Domecile.get_summary_of_postcode(request.GET['postcode'])
        contacts_count = Contact.objects.filter(
                domecile__postcode_point=PostcodeMapping.match_postcode(request.GET['postcode'])).count()
        data = {'postcode': request.GET['postcode'], 'summary': summary[0], 'buildings': summary[1],
                'contacts': contacts_count}
    except:
        data = {'postcode': request.GET['postcode'], 'summary': 'No data found', 'buildings': 0, 'contacts': 0}
    return JsonResponse(data=data)


class HomepageView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        from campaigns.models import Campaign
        kwargs['current_campaign'] = Campaign.get_latest_top_level_campaign()
        return super(HomepageView, self).get_context_data(**kwargs)


class LoginTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'why_canvass.html'
