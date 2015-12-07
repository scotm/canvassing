from django.contrib import admin
from django import forms
from polling.models import CanvassQuestion, CanvassChoicesAvailable, CanvassQuestionaire


class CanvassChoicesAdminForm(forms.ModelForm):
    class Meta:
        model = CanvassChoicesAvailable
        fields = ('question', 'option',)

    def __init__(self, *args, **kwargs):
        super(CanvassChoicesAdminForm, self).__init__(*args, **kwargs)
        print self.fields
        self.fields['question'].queryset = self.fields['question'].queryset.filter(type='Multiple-choice')
        if self.instance and self.instance.pk:
            self.fields['question'].queryset = self.fields['question'].queryset.filter(pk=self.instance.question.pk)
            self.fields['question'].widget = forms.HiddenInput()


class CanvassChoicesAdmin(admin.ModelAdmin):
    form = CanvassChoicesAdminForm


class CanvassQuestionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'polling_question')


admin.site.register(CanvassQuestion, CanvassQuestionAdmin)
admin.site.register(CanvassChoicesAvailable, CanvassChoicesAdmin)
admin.site.register(CanvassQuestionaire)
