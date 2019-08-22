from django import forms
from .models import *
from campus_ambassador.models import *
from django.forms import BaseFormSet

class ParticipantRegistrationDetailsForm(forms.ModelForm):

    referring_ca = forms.CharField(required=False, widget=forms.TextInput, label='CA Refferal Code')

    class Meta:
        model = Participant
        fields = ['college', 'mobile_number', 'referring_ca']

    def clean_referring_ca(self):
        referring_ca_code = self.cleaned_data['referring_ca'].strip().upper()
        print(referring_ca_code)
        if referring_ca_code == '':
            referring_ca_code = None
        else:
            try:
                referring_ca_code = RegistrationDetails.objects.get(campus_ambassador_code=referring_ca_code)
            except RegistrationDetails.DoesNotExist:
                raise forms.ValidationError(message="Please enter a valid CA Referral Code!", code="InvalidCampusAmbassadorReferralCode")
        return referring_ca_code


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name']


class TeamHasMemberForm(forms.Form):

    team_member = forms.CharField(label="Member Participant Code")

    def clean(self):
        self.cleaned_data = super().clean()
        try:
            team_member = self.cleaned_data['team_member'].upper()
            obj = Participant.objects.get(participant_code=team_member)
            self.cleaned_data['team_member'] = obj
            return self.cleaned_data
        except:
            err_message = "Please enter a valid Participant Code!"
            self.add_error('team_member', err_message)


class BaseTeamFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        team_members = set()
        for form in self.forms:
            team_member = form.cleaned_data.get('team_member')
            if team_member == None:
                continue
            if team_member in team_members:
                raise forms.ValidationError("Cannot have same participants in a team.")
            team_members.add(team_member)
