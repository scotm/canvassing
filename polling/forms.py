from django.forms import ModelForm

from polling.models import CanvassQuestionaire


class QuestionaireForm(ModelForm):
    class Meta:
        model = CanvassQuestionaire
        fields = ['campaign', 'questions']
