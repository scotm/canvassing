from braces.views import LoginRequiredMixin
from json_views.views import JSONDataView

from campaigns.models import Signature, Campaign


__author__ = 'scotm'
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView

from campaigns.forms import ContactFindForm
from core.models import Contact, PoliticalParty
from leafleting.models import CanvassRun


class FindContactList(ListView):
    model = Contact
    template_name = 'sign_petition.html'
    form = ContactFindForm

    def get_queryset(self):
        form = ContactFindForm(self.request.GET)
        queryset = self.model.objects.none()
        if form.is_valid():
            queryset = Contact.objects.filter(first_name__istartswith=form.cleaned_data['first_name'],
                                              surname__iexact=form.cleaned_data['last_name'],
                                              domecile__postcode__iexact=form.cleaned_data['postcode'])
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form(self.request.GET) if self.request.GET else self.form()
        return super(FindContactList, self).get_context_data(**kwargs)


class CanvassDataInput(DetailView):
    template_name = 'data_input.html'
    model = CanvassRun

    def get_queryset(self):
        return super(CanvassDataInput, self).get_queryset()

    def get_context_data(self, **kwargs):
        return super(CanvassDataInput, self).get_context_data(**kwargs)


# class CanvassRunFind(LoginRequiredMixin, FilterView):
#     template_name = 'canvassrun_find.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs.update({'user_runs': CanvassRun.objects.filter(booked_by=self.request.user)})
#         return super(CanvassRunFind, self).get_context_data(**kwargs)


class SignPetition(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        try:
            contact_pk = int(self.request.GET['contact'])
            contact = Contact.objects.get(pk=contact_pk)
        except:
            return
        signature = Signature.objects.filter(contact=contact).first()
        if signature:
            signature.delete()
            return {'status': 'deleted'}
        else:
            # TODO: Need to retrieve the campaign from the request, too.
            # TODO: Stash the chosen campaign and store it in the session variable.
            Signature.objects.create(contact=contact, campaign=Campaign.get_latest_top_level_campaign())
            return {'status': 'signed'}

