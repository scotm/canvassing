from django.contrib import admin
from django import forms

from polling.models import CanvassQuestion, CanvassChoicesAvailable


class CanvassChoicesAdminForm(forms.ModelForm):
    class Meta:
        model = CanvassChoicesAvailable
        fields = ('question', 'option',)

    def __init__(self, *args, **kwargs):
        super(CanvassChoicesAdminForm, self).__init__(*args, **kwargs)
        print self.fields
        self.fields['question'].queryset = self.fields['question'].queryset.filter(type='choice')
        if self.instance and self.instance.pk:
            self.fields['question'].queryset = self.fields['question'].queryset.filter(pk=self.instance.question.pk)
            self.fields['question'].widget = forms.HiddenInput()


class CanvassChoicesAdmin(admin.ModelAdmin):
    form = CanvassChoicesAdminForm


admin.site.register(CanvassQuestion)
admin.site.register(CanvassChoicesAvailable, CanvassChoicesAdmin)
