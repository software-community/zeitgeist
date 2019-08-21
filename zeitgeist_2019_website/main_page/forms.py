from django import forms
from .models import *
from campus_ambassador.models import *

class ParticipantRegistrationDetailsForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['mobile_number', 'referring_ca']
        widgets = {
            'mobile_number' : forms.TextInput(),
        }


class TeamRegistrationDetailsForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        wdigets = {
            'name' : forms.TextInput()
        }
