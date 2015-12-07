# Create your views here.
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, RedirectView
from django.contrib import messages
import django_filters
from django_filters.views import FilterView
from braces.views import LoginRequiredMixin
from json_views.views import JSONDataView
from core.models import Ward, Region
from leafleting.models import LeafletRun, CanvassRun
from postcode_locator.models import PostcodeMapping

users = {k.pk: k for k in get_user_model().objects.all()}


class UserFilter(django_filters.ChoiceFilter):
    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.name).values_list(self.name, flat=True)
        self.extra['choices'] = [("", "All")] + [(o, users[o]) for o in users]
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
        return CanvassRun.get_unbooked_available_runs(user=self.request.user).select_related('created_by', 'ward',
                                                                                             'bookedcanvassrun')


class CanvassRunDelete(LoginRequiredMixin, DeleteView):
    model = CanvassRun
    success_url = reverse_lazy('canvass_list')


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

        if 'questionaire' in self.request.GET:
            leaflet_run.questionaire_id = int(self.request.GET['questionaire'])

        leaflet_run.ward = leaflet_run.get_ward()
        leaflet_run.save()
        context.update({'outcome': 'success'})
        return context


class CanvassRunCreate(LeafletRunCreate):
    model = CanvassRun


class CanvassRunBook(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        c = CanvassRun.objects.get(pk=self.kwargs['pk'])
        c.book(self.request.user)
        messages.add_message(self.request, messages.INFO, 'CanvassRun: %s booked' % (unicode(c)))
        return reverse('canvass_list')


class CanvassRunUnbook(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        c = CanvassRun.objects.get(pk=self.kwargs['pk'])
        c.unbook()
        messages.add_message(self.request, messages.INFO, 'CanvassRun: %s released' % (unicode(c)))
        return reverse('canvass_list')


# TODO: Unusable
class LeafletRunEdit(LoginRequiredMixin, UpdateView):
    model = LeafletRun


class LeafletHomepage(LoginRequiredMixin, TemplateView):
    runs_limit = 5
    run_klass = LeafletRun
    template_name = 'leafleting_homepage.html'

    def get_runs(self):
        return self.run_klass.objects.all()[:self.runs_limit]

    def get_context_data(self, **kwargs):
        kwargs['runs'] = self.get_runs()
        return super(LeafletHomepage, self).get_context_data(**kwargs)


class CanvassHomepage(LeafletHomepage):
    run_klass = CanvassRun
    template_name = 'canvassing_homepage.html'

    def get_runs(self):
        return self.run_klass.get_unbooked_available_runs()[:self.runs_limit]


class RunDetailView(LoginRequiredMixin, DetailView):
    pass


class PrintRunDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leafleting/print_canvassrun_detail.html'

    def get_queryset(self):
        return super(PrintRunDetailView, self).get_queryset().prefetch_related('questionaire__questions')


class RunPicker(LoginRequiredMixin, DetailView):
    pass


class CanvassPicker(RunPicker):
    template_name = 'canvassing_picker.html'

    def get_context_data(self, **kwargs):
        from polling.models import CanvassQuestionaire
        kwargs['questionaires'] = CanvassQuestionaire.objects.all()
        return super(RunPicker, self).get_context_data(**kwargs)


class AreaPicker(LoginRequiredMixin, ListView):
    model = Ward
    template_name = 'leafleting_ward_picker.html'

    def get_queryset(self):
        return super(AreaPicker, self).get_queryset().filter(active=True)


class UserCanvassRunFind(LoginRequiredMixin, ListView):
    model = CanvassRun
    template_name = 'canvassrun_find.html'

    def get_queryset(self):
        return super(UserCanvassRunFind, self).get_queryset().filter(bookedcanvassrun__booked_by=self.request.user)


class DataInput(PrintRunDetailView):
    model = CanvassRun
    template_name = 'data_input.html'
