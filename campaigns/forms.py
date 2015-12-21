from django import forms
from django.core.exceptions import ValidationError

from postcode_locator.models import PostcodeMapping


class ContactFindForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Surname', max_length=100)
    postcode = forms.CharField(label='Postcode', max_length=10)

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        if not PostcodeMapping.match_postcode(postcode, raise_exceptions=False):
            raise ValidationError("Postcode not found")
        return postcode
