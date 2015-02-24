from django.views.generic import DetailView, ListView

from core.models import Contact


class ContactView(DetailView):
    model = Contact

class ContactListView(ListView):
    model = Contact