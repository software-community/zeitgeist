import hashlib
import hmac
import os
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse
from urllib.parse import urlparse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from .methods import payment_request
from django.forms import formset_factory
# Create your views here.


def main_page_home(request):
    context={'title':'Zeitgeist'}
    return render(request, 'main_page/index.html',context)


def change_account(request):
    '''
    If some other page redirects us to change_account, then 404 will happen
    but why will some other page redirect to here
    '''
    prev_page = request.META.get('HTTP_REFERER', reverse('main_page_home'))
    _next = urlparse(prev_page).path
    logout(request)
    return redirect(reverse('google_login')+'?next='+_next)


@login_required
def register_as_participant(request):

    try:
        prev_participant_registration_details = Participant.objects.get(participating_user=request.user)
    except Participant.DoesNotExist:
        prev_participant_registration_details = None

    if prev_participant_registration_details:
        return render(request, 'main_page/messages.html',context={'already_registered':'already_registered'})

    request.user.email = SocialAccount.objects.get(
        user=request.user).extra_data.get("email")
    request.user.save()

    if request.method == "POST":
        participant_registration_details_form = ParticipantRegistrationDetailsForm(
            request.POST)
        if participant_registration_details_form.is_valid():
            new_participant_registration = participant_registration_details_form.save(
                commit=False)
            new_participant_registration.participating_user = request.user
            new_participant_registration.participant_code = (str(request.user.first_name)[
                :4]).upper() + str(request.user.id) + 'Z19'
            new_participant_registration.save()
            # send_mail(
            #     'Welcome to Zeitgeist 2k19',
            #     'Dear ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + '\n\nThank you for showing your interest in Zeitgeist 2k19. We are excited for your journey with us and wish you luck for all the events that you take part in.\n\nYour PARTICIPANT CODE is ' + str(
            #         new_participant_registration.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR code.\n\nWe wish you best of luck. Give your best and earn exciting prizes !!!\n\nRegards\nZeitgeist 2k19 Public Relations Team',
            #     'zeitgeist.pr@iitrpr.ac.in',
            #     [request.user.email],
            #     fail_silently=False,
            # )
            return redirect('main_page_events')
    else:
        participant_registration_details_form = ParticipantRegistrationDetailsForm()

    return render(request, 'main_page/register_as_participant.html',
                    {'participant_registration_details_form': participant_registration_details_form})


def main_page_events(request):

    events_data = {}
    categories = Category.objects.all()
    for category in categories:
        events_data[category] = {}
        subcategories = category.subcategory_set.all()
        for subcategory in subcategories:
            events_data[category][subcategory] = subcategory.event_set.all()

    return render(request, 'main_page/events.html', {'events_data': events_data})


@login_required
def register_for_event(request, event_id):

    try:
        participant = Participant.objects.get(participating_user=request.user)
    except Participant.DoesNotExist:
        return redirect('register_as_participant')

    event = Event.objects.get(id=event_id)

    if event.event_type == 'Solo':
        try:
            payment_details = ParticipantHasPaid.objects.get(participant=participant, paid_subcategory=event.subcategory)
            if payment_details.transaction_id == '-1' or payment_details.transaction_id == '0':
                return redirect('pay_for_subcategory', subcategory_id=event.subcategory.id)
        except ParticipantHasPaid.DoesNotExist:
            return redirect('pay_for_subcategory', subcategory_id=event.subcategory.id)
        ParticipantHasParticipated.objects.create(participant=participant, event=event)
        # send_mail(
        #     'Participation in ' + str(event.name) + ' in Zeitgeist 2k19',
        #     'Dear ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + '\n\nThank you for participating in ' + str(event.name) + '. Please carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nRemider - Your PARTICIPANT CODE is ' + str(
        #         participant.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR code.\n\nRegards\nZeitgeist 2k19 Public Relations Team',
        #     'zeitgeist.pr@iitrpr.ac.in',
        #     [request.user.email],
        #     fail_silently=False,
        # )
        return render(request,'main_page/messages.html',context={'message':f"Your Registration for the Event: {event.name} is succesfull"})

    else:
        TeamHasMemberFormSet = formset_factory(form=TeamHasMemberForm, formset=BaseTeamFormSet, extra=event.maximum_team_size-1, max_num=event.maximum_team_size, validate_max=True, min_num=event.minimum_team_size, validate_min=True)
        if request.method == "POST":
            print(request.POST)
            team_member_formset = TeamHasMemberFormSet(request.POST, initial=[{'team_member' : str(participant.participant_code)}],prefix='team_member')
            team_form = TeamForm(request.POST)
            if team_member_formset.is_valid() and team_form.is_valid():
                for team_member_form in team_member_formset:
                    try:
                        team_member_payment = ParticipantHasPaid.objects.get(participant=team_member_form.team_member, paid_subcategory=event.subcategory)
                        if team_member_payment.transaction_id == '-1' or team_member_payment.transaction_id == '0':
                            return render(request,'main_page/messages.html',context={'message':"Some of the team members have not paid for the subcategory !!! Try again when all the team members have paid for the subcategory."})
                            # return HttpResponse()
                    except ParticipantHasPaid.DoesNotExist:
                        return render(request,'main_page/messages.html',context={'message':"Some of the team members have not paid for the subcategory !!! Try again when all the team members have paid for the subcategory."})
                        # return HttpResponse("Some of the team members have not paid for the subcategory !!! Try again when all the team members have paid for the subcategory.")
                    # if form is empty
                    except:
                        continue
                print(team_form.cleaned_data)
                alpha_name=team_form.cleaned_data['name']
                new_team = team_form.save(commit=False)
                temp_team_code = str(request.user.id) + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                new_team.team_code = temp_team_code
                new_team.event = event
                new_team.captain = participant
                new_team.save()
                new_team = Team.objects.get(name=alpha_name, team_code=temp_team_code, event=event, captain=participant)
                new_team_code = ((str(new_team.name).replace(" ", ""))[:4]).upper() + str(new_team.id) + 'Z19'
                new_team.team_code = new_team_code
                new_team.save()
                new_team = Team.objects.get(team_code=new_team_code)
                # ParticipantHasParticipated.objects.create(participant=participant, event=event)
                # TeamHasMember.objects.create(team=new_team, member=participant)
                for team_member_form in team_member_formset:
                    team_member = Participant.objects.get(participant_code=team_member_form.cleaned_data['team_member'])
                    ParticipantHasParticipated.objects.create(participant=team_member, event=event)
                    TeamHasMember.objects.create(team=new_team, member=team_member)
                # send_mail(
                #     'Welcome to Zeitgeist 2k19',
                #     'Dear ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + '\n\nThank you for showing your interest in Zeitgeist 2k19. We are excited for your journey with us and wish you luck for all the events that you take part in.\n\nYour PARTICIPANT CODE is ' + str(
                #         new_participant_registration.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR code.\n\nWe wish you best of luck. Give your best and earn exciting prizes !!!\n\nRegards\nZeitgeist 2k19 Public Relations Team',
                #     'zeitgeist.pr@iitrpr.ac.in',
                #     [request.user.email],
                #     fail_silently=False,
                # )
                return render(request,'main_page/messages.html',context={'message':f"Your Registration for the Event: {event.name} is succesfull"})
        else:
            team_form = TeamForm()
            team_member_formset = TeamHasMemberFormSet(initial=[{'team_member' : str(participant.participant_code)}],prefix='team_member')

        return render(request, 'main_page/register_team.html',
                        {
                            'team_form': team_form,
                            'team_member_formset': team_member_formset,
                            })


@login_required
def pay_for_subcategory(request, subcategory_id):

    try:
        participant = Participant.objects.get(participating_user=request.user)
    except:
        return redirect('register_as_participant')

    subcategory = Subcategory.objects.get(id=subcategory_id)

    response = payment_request(subcategory.participation_fees_per_person, subcategory.name, request.user.email)
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']
        participanthaspaid = ParticipantHasPaid.objects.create(participant=participant,
                                                               paid_subcategory=subcategory, payment_request_id=payment_request_id)
        return redirect(url)
    else:
        return HttpResponseServerError()


def weebhook(request):

    if request.method == "POST":
        print(request.POST)
        data = request.POST
        mac_provided = data.pop('mac')

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))

        mac_calculated = hmac.new(
            os.getenv('private_salt'), message, hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                participantpaspaid = ParticipantHasPaid.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    participantpaspaid.transaction_id = data['payment_id']
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    participantpaspaid.transaction_id = '0'
                participantpaspaid.save()
            except Exception as err:
                print(err)


def payment_redirect(request):
    if request.method == "POST":
        print(request.POST)
