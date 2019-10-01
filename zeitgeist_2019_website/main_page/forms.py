from django import forms
from .models import *
from campus_ambassador.models import *
from django.forms import BaseFormSet


class ParticipantRegistrationDetailsForm(forms.ModelForm):

    referring_ca = forms.CharField(required=False, widget=forms.TextInput, label='CA Refferal Code')

    class Meta:
        model = Participant
        fields = ['name', 'college_name', 'college_city', 'personal_address_with_pin_code', 'contact_mobile_number', 'whatsapp_mobile_number', 'birth_date', 'referring_ca']

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
        if self.forms[0].has_changed():
            captain_participation_code = self.forms[0].initial['team_member']
            msg = "You must fill " + str(captain_participation_code) + " here!"
            self.forms[0].add_error('team_member', forms.ValidationError(message=msg, code="CaptainChanged"))
        team_members = set()
        for form in self.forms:
            team_member = form.cleaned_data.get('team_member')
            # if form was not even filled
            if not team_member:
                continue
            if team_member in team_members:
                msg = "Each participant in a team must be unique!"
                form.add_error('team_member', forms.ValidationError(message=msg, code="SameParticipant"))
            team_members.add(team_member)


class AccomodationForm(forms.ModelForm):

    participant = forms.CharField(required=True, widget=forms.TextInput, label='Participant Code')

    class Meta:
        model = Accomodation
        fields = ['participant', 'gender', 'acco_for_day_one', 'acco_for_day_two', 'acco_for_day_three', 'include_meals']

    def clean_participant(self):
        participant_code = self.cleaned_data['participant'].strip().upper()
        try:
            participant_code = Participant.objects.get(participant_code=participant_code)
        except Participant.DoesNotExist:
            raise forms.ValidationError(message="Please enter a valid Participant Code!", code="InvalidParticipantCode")
        return participant_code

    def clean(self):
        cleaned_data = super().clean()
        ad1 = cleaned_data.get("acco_for_day_one")
        ad2 = cleaned_data.get("acco_for_day_two")
        ad3 = cleaned_data.get("acco_for_day_three")
        # if accomodation for no day is selected
        if not (ad1 or ad2 or ad3):
            raise forms.ValidationError("Atleast one of the three nights should be selected")
