from django import forms
from .models import *

class CampusAmbassadorRegistrationDetailsForm(forms.ModelForm):
    class Meta:
        model = RegistrationDetails
        fields = ['college', 'mobile_number', 'why_interested',
            'past_experience']
        widgets = {
            'college': forms.TextInput(),
            'mobile_number' : forms.TextInput(),
            'why_interested' : forms.TextInput(),
            'past_experience' : forms.TextInput()
        }
