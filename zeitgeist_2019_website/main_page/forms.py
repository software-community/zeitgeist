from django import forms
from .models import *

class ParticipantRegistrationDetailsForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['mobile_number']
        widgets = {'mobile_number' : forms.TextInput()}

class TeamRegistrationDetailsForm(form.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'captain']
