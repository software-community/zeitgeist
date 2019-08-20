from django import forms
from .models import *

class ParticipantRegistrationDetailsForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['mobile_number', 'referring_ca']
        widgets = {
            'mobile_number' : forms.TextInput(),
            # 'referring_ca' : forms.ModelChoiceField(),
        }


class TeamRegistrationDetailsForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        wdigets = {
            'name' : forms.TextInput()
        }
