from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView, ListView
from core.models import Ward

class WardListView(ListView):
    model = Ward
    template_name = 'leafleting/ward_list.html'

    def get_queryset(self):
        return super(WardListView, self).get_queryset()


class WardView(DetailView):
    model = Ward
    template_name = 'leafleting/ward_view.html'

    def get_context_data(self, **kwargs):
        context = super(WardView, self).get_context_data(**kwargs)

        return context