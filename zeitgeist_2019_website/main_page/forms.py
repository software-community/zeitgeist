from django import forms
from .models import *
from campus_ambassador.models import *
from django.shortcuts import get_object_or_404

class ParticipantRegistrationDetailsForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = ['mobile_number', 'referring_ca']
        widgets = {
            'mobile_number' : forms.TextInput(),
            'referring_ca' : forms.TextInput(),
        }

    def clean(self):
        # complete this
        pass


class TeamRegistrationDetailsForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name']
        wdigets = {
            'name' : forms.TextInput()
        }
