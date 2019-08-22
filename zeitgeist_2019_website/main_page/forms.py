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

    team_member = forms.CharField(label="Member Participant Code", required=True)

    def clean_team_member(self):
        team_member_code = self.cleaned_data['team_member'].strip().upper()
        try:
            team_member_code = Participant.objects.get(participant_code=team_member_code)
        except Participant.DoesNotExist:
            raise forms.ValidationError(message="Please enter a valid Participant Code!", code="InvalidParticipantCode")
        return team_member_code


class BaseTeamFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        team_members = set()
        for form in self.forms:
            try:
                team_member = form.cleaned_data.get('team_member')
            # this form was not intended to be submitted
            except:
                continue
            if team_member in team_members:
                raise forms.ValidationError(message="Cannot have same participants in one team!", code="SameParticipant")
            team_members.add(team_member)
