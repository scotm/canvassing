from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from polling.models import CanvassQuestionaire, CanvassQuestion

__author__ = 'scotm'


class QuestionaireListView(ListView):
    model = CanvassQuestionaire

class QuestionaireCreateView(CreateView):
    template_name = 'polling/canvassquestionaire_create.html'
    model = CanvassQuestionaire
    fields = ['campaign', 'questions']
    success_url = reverse_lazy('questionaire_list')

class QuestionCreateView(CreateView):
    template_name = 'polling/canvassquestion_create.html'
    model = CanvassQuestion
    fields = ['short_name', 'polling_question', 'type']
    success_url = reverse_lazy('questionaire_create')
