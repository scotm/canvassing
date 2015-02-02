from django.views.generic import DetailView

from core.models import Contact


class ContactView(DetailView):
    model = Contact
