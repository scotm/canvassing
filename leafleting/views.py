from collections import defaultdict
from functools import partial
from urlparse import parse_qs

import django_filters
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, RedirectView
from django_filters.views import FilterView

from core.models import Ward, Contact, Domecile, Region
from leafleting.models import LeafletRun, CanvassRun
from polling.models import CanvassQuestion, CanvassChoice, CanvassTrueFalse, CanvassLongAnswer, CanvassRange, \
    CanvassQuestionaire
from postcode_locator.models import PostcodeMapping

try:
    users = {k.pk: k for k in get_user_model().objects.all()}
except:
    users = {}

answer_types = {'Multiple-choice': CanvassChoice, 'True/False': CanvassTrueFalse,
                'Detailed Answer': CanvassLongAnswer, 'Range': CanvassRange}

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


def canvass_run_create(request, model=CanvassRun):
    postcodes = request.POST.getlist('selected_postcodes[]')
    if not postcodes:
        return HttpResponseNotFound('<h1>A list of postcodes is required</h1>')
    else:
        run = model.objects.create(
                **{'name': request.POST['run_name'], 'notes': request.POST['run_notes'], 'created_by': request.user})
        for x in postcodes:
            run.postcode_points.add(PostcodeMapping.match_postcode(x))

        if 'questionaire' in request.POST:
            run.questionaire_id = int(request.POST['questionaire'])

        run.ward = run.get_ward()
        run.save()
        return JsonResponse(data={'outcome': 'success'})


leaflet_run_create = partial(canvass_run_create, model=LeafletRun)


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


@login_required
def data_input_acceptor(request):
    old_data = request.POST['data']
    parsed_data = parse_post_data(old_data)
    delete_values, errors = create_answer_objects(parsed_data)
    return JsonResponse(data={'data': delete_values, 'errors': errors})


def create_answer_objects(parsed_data):
    delete_values, errors = [], []
    for contact_pk, value in parsed_data.iteritems():
        contact = Contact.objects.get(pk=contact_pk)
        for descriptor, answer in value.iteritems():
            try:
                if descriptor.startswith('question_'):
                    question = CanvassQuestion.objects.get(pk=int(descriptor.replace('question_', '')))
                    klass = answer_types[question.type]
                    klass.store_response(contact=contact, question=question, answer=answer)
            except TypeError:
                raise
            except Exception as e:
                errors.append(": ".join([e.__class__.__name__, e.message]))
        delete_values.append(contact_pk)
    return delete_values, errors


def parse_post_data(post_data):
    data = parse_qs(post_data)
    parsed_data = defaultdict(dict)
    for key, value in data.iteritems():
        contact_pk, argument = tuple(key.split('_', 1))
        parsed_data[contact_pk][argument] = value[0]
    return parsed_data


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
