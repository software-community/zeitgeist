from django import forms
from .models import *
from campus_ambassador.models import *
from django.shortcuts import get_object_or_404

class ParticipantRegistrationDetailsForm(forms.ModelForm):

    referring_ca = forms.CharField(required=False, widget=forms.TextInput, label='CA Refferal Code')

    class Meta:
        model = Participant
        fields = ['mobile_number', 'referring_ca']

    def clean(self):
        self.cleaned_data = super().clean()
        if self.data['referring_ca'] == '':
            self.cleaned_data['referring_ca'] = None
            return self.cleaned_data
        try:
            obj = get_object_or_404(RegistrationDetails, campus_ambassador_code=self.data['referring_ca'])
            self.cleaned_data['referring_ca'] = obj
            return self.cleaned_data
        except:
            msg = "Not a Valid CA Refferal Code!"
            self.add_error('referring_ca', msg)


class TeamRegistrationDetailsForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name']
        wdigets = {
            'name' : forms.TextInput()
        }
