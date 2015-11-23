# Create your views here.
from django.db import models
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, TemplateView, UpdateView

import django_filters
from django_filters.views import FilterView
from braces.views import LoginRequiredMixin
from json_views.views import JSONDataView

from core.models import Ward, Region
from leafleting.models import LeafletRun, CanvassRun
from postcode_locator.models import PostcodeMapping

users = {k.pk:k for k in get_user_model().objects.all()}

class UserFilter(django_filters.ChoiceFilter):
    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.name).values_list(self.name, flat=True)
        self.extra['choices'] = [("", "All")] + [(o, users[o]) for o in qs]
        return super(django_filters.ChoiceFilter, self).field


class AnyAllValuesFilter(django_filters.AllValuesFilter):
    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.name).values_list(self.name, flat=True)
        self.extra['choices'] = [("", "All")] + [(o, o) for o in qs]
        return super(django_filters.AllValuesFilter, self).field


class CanvassRunFilter(django_filters.FilterSet):
    filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_type': 'icontains',
            }
        }
    }
    ward__ward_name = AnyAllValuesFilter()
    ward__local_authority_name = AnyAllValuesFilter()
    created_by = UserFilter()

    class Meta:
        model = CanvassRun
        fields = ['name', 'ward__ward_name', 'ward__local_authority_name', 'created_by']


class CanvassRunListView(LoginRequiredMixin, FilterView):
    filterset_class = CanvassRunFilter
    template_name = 'leafleting/canvassrun_list.html'
    model = CanvassRun

    def get_queryset(self):
        return super(CanvassRunListView, self).get_queryset().select_related('created_by', 'ward')

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


class RunDetailView(LoginRequiredMixin, DetailView):
    pass


class RunPicker(LoginRequiredMixin, DetailView):
    pass


class AreaPicker(LoginRequiredMixin, ListView):
    model = Ward
    template_name = 'leafleting_ward_picker.html'

    def get_queryset(self):
        return super(AreaPicker, self).get_queryset().filter(active=True)
