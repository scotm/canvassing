from braces.views import LoginRequiredMixin
from django.views.generic import ListView
from json_views.views import JSONDataView

from campaigns.forms import ContactFindForm
from campaigns.models import Signature, Campaign
from core.models import Contact

__author__ = 'scotm'


class FindContactList(ListView):
    model = Contact
    template_name = 'sign_petition.html'
    form = ContactFindForm

    def get_queryset(self):
        form = ContactFindForm(self.request.GET)
        queryset = self.model.objects.none()
        if form.is_valid():
            queryset = self.model.objects.filter(first_name__istartswith=form.cleaned_data['first_name'],
                                                 surname__iexact=form.cleaned_data['last_name'],
                                                 domecile__postcode__iexact=form.cleaned_data['postcode'])
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form(self.request.GET) if self.request.GET else self.form()
        kwargs['campaigns'] = Campaign.objects.all()
        return super(FindContactList, self).get_context_data(**kwargs)


class GetPetition(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        try:
            signature = Signature.objects.filter(contact__pk=self.request.GET['contact'],
                                                 campaign__pk=self.request.GET['campaign']).first()
        except:
            return
        return {'result': True if signature else False}


class SignPetition(LoginRequiredMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        try:
            campaign = Campaign.objects.get(pk=self.request.GET['campaign'])
            contact = Contact.objects.get(pk=int(self.request.GET['contact']))
            self.request.session['campaign'] = int(self.request.GET['campaign'])
        except:
            return
        signature = Signature.objects.filter(contact=contact, campaign=campaign).first()
        if signature:
            signature.delete()
            return {'status': 'deleted'}
        else:
            # TODO: Need to retrieve the campaign from the request, too.
            # TODO: Stash the chosen campaign and store it in the session variable.
            Signature.objects.create(contact=contact, campaign=campaign)
            return {'status': 'signed'}
