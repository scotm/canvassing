from django.contrib.auth import authenticate
from functools import cmp_to_key
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin

from django.views.generic import DetailView, ListView, TemplateView
from json_views.views import JSONDataView

from core.models import Contact, Domecile, Ward


def login_user(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('homepage'))
    return render_to_response('account_auth/login.html', context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


class ContactView(LoginRequiredMixin, DetailView):
    model = Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    paginate_by = 100


class DomecileMapView(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(DomecileMapView, self).get_context_data(**kwargs)
        region = self.request.GET['region']
        bbox = self.request.GET['BBox'].split(',')
        queryset = Domecile.get_postcode_points(southwest=(bbox[0], bbox[1]), northeast=(bbox[2], bbox[3]),
                                                region=Ward.objects.get(pk=int(region)))
        data = [{'postcode':x.postcode, 'point':x.postcode_point.point} for x in queryset]
        context.update({'data':data})
        return context


class DomecileAddressView(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(DomecileAddressView, self).get_context_data(**kwargs)
        postcode = self.request.GET['postcode']
        data = Domecile.get_sorted_addresses(postcode)
        context.update({'data':data, 'postcode':postcode})
        return context


class WardListView(LoginRequiredMixin, ListView):
    model = Ward

    def get_queryset(self):
        return super(WardListView, self).get_queryset()


class WardView(LoginRequiredMixin, DetailView):
    model = Ward

    def get_context_data(self, **kwargs):
        return super(WardView, self).get_context_data(**kwargs)

class HomepageView(LoginRequiredMixin, TemplateView):
    template_name='homepage.html'

    def get_context_data(self, **kwargs):
        from campaigns.models import Campaign
        kwargs.update({'current_campaign':Campaign.get_latest_top_level_campaign()})
        return super(HomepageView, self).get_context_data(**kwargs)

