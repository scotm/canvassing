from __future__ import print_function
# Create your views here.
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from json_views.views import JSONDataView
from core.models import Ward

from leafleting.models import LeafletRun, CanvassRun
from postcode_locator.models import PostcodeMapping

from django_filters.views import FilterView
from django_filters import FilterSet, AllValuesFilter, ChoiceFilter


class UserFilter(ChoiceFilter):
    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.name).values_list(self.name, flat=True)
        self.extra['choices'] = [("", "All")] + [(o, str(get_user_model().objects.get(pk=o))) for o in qs]
        return super(ChoiceFilter, self).field

class AnyAllValuesFilter(AllValuesFilter):
    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.name).values_list(self.name, flat=True)
        self.extra['choices'] = [("", "All")] + [(o, o) for o in qs]
        return super(AllValuesFilter, self).field

class CanvassRunFilter(FilterSet):
    ward__ward_name = AnyAllValuesFilter()
    ward__local_authority_name = AnyAllValuesFilter()
    created_by = UserFilter()
    class Meta:
        model = CanvassRun
        fields = ['name', 'ward__ward_name', 'ward__local_authority_name', 'created_by']

class CanvassRunListView(FilterView):
    filterset_class = CanvassRunFilter
    template_name = 'leafleting/canvassrun_list.html'

    def get_context_data(self, **kwargs):
        context = super(CanvassRunListView, self).get_context_data(**kwargs)
        return context


class LeafletRunListView(LoginRequiredMixin, ListView):
    model = LeafletRun


class LeafletRunCreate(LoginRequiredMixin, JSONDataView):
    model = LeafletRun

    def get_context_data(self, **kwargs):
        context = super(LeafletRunCreate, self).get_context_data(**kwargs)
        postcodes = self.request.GET.getlist('selected_postcodes[]')
        if not postcodes:
            raise Exception("A list of postcodes is required.")

        leaflet_run = self.model.objects.create(
            **{'name': self.request.GET['run_name'], 'notes': self.request.GET['run_notes'],
               'created_by': self.request.user})
        for x in postcodes:
            leaflet_run.postcode_points.add(PostcodeMapping.match_postcode(x))

        leaflet_run.ward = leaflet_run.get_ward()
        leaflet_run.save()
        context.update({'outcome': 'success'})
        return context


class CanvassRunCreate(LeafletRunCreate):
    model = CanvassRun


# TODO: Unusable
class LeafletRunEdit(LoginRequiredMixin, UpdateView):
    model = LeafletRun


class LeafletHomepage(LoginRequiredMixin, TemplateView):
    run_klass = LeafletRun
    template_name = 'leafleting_homepage.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'runs': self.run_klass.objects.all()[:5]})
        return super(LeafletHomepage, self).get_context_data(**kwargs)


class CanvassHomepage(LeafletHomepage):
    run_klass = CanvassRun
    template_name = 'canvassing_homepage.html'


class LeafletRunDetailView(LoginRequiredMixin, DetailView):
    model = LeafletRun


class CanvassRunDetailView(LeafletRunDetailView):
    model = CanvassRun


class LeafletingPicker(LoginRequiredMixin, DetailView):
    model = Ward
    template_name = 'leafleting_picker.html'


class LeafletWardPicker(LoginRequiredMixin, ListView):
    model = Ward
    template_name = 'leafleting_ward_picker.html'

    def get_queryset(self):
        return super(LeafletWardPicker, self).get_queryset().filter(active=True)
