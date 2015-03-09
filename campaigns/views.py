from django.views.generic.edit import FormMixin

from campaigns.forms import ContactFindForm
from core.models import Contact


__author__ = 'scotm'
from django.views.generic import ListView


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

