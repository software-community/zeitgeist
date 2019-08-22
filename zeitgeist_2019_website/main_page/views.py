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
        return render(request, 'main_page/already_registered_as_participant.html')

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
        return HttpResponse("Success")

    else:
        TeamHasMemberFormSet = formset_factory(form=TeamHasMemberForm, formset=BaseTeamFormSet, extra=event.maximum_team_size-1, max_num=event.maximum_team_size, validate_max=True, min_num=event.minimum_team_size, validate_min=True)
        if request.method == "POST":
            team_member_formset = TeamHasMemberFormSet(request.POST, initial=[{'team_member' : str(participant.participant_code)}])
            team_form = TeamForm(request.POST)
            if team_member_formset.is_valid() and team_form.is_valid():
                for team_member_form in team_member_formset:
                    try:
                        team_member_payment = ParticipantHasPaid.objects.get(participant=team_member_form.team_member, paid_subcategory=event.subcategory)
                        if team_member_payment.transaction_id == '-1' or team_member_payment.transaction_id == '0':
                            return HttpResponse("Some of the team members have not paid for the subcategory !!! Try again when all the team members have paid for the subcategory.")
                    except ParticipantHasPaid.DoesNotExist:
                        return HttpResponse("Some of the team members have not paid for the subcategory !!! Try again when all the team members have paid for the subcategory.")
                    # if form is empty
                    except:
                        continue
                new_team = team_form.save(commit=False)
                temp_team_code = str(request.user.id) + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                new_team.team_code = temp_team_code
                new_team.event = event
                new_team.captain = participant
                new_team.save()
                new_team = Team.objects.get(name=team_form.name, team_code=temp_team_code, event=event, captain=participant)
                new_team_code = ((str(new_team.name).replace(" ", ""))[:4]).upper() + str(new_team.id) + 'Z19'
                new_team.team_code = new_team_code
                new_team.save()
                new_team = Team.objects.get(team_code=new_team_code)
                # ParticipantHasParticipated.objects.create(participant=participant, event=event)
                # TeamHasMember.objects.create(team=new_team, member=participant)
                for team_member_form in team_member_formset:
                    team_member = Participant.objects.get(participant_code=team_member_form.team_member)
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
                return HttpResponse("Success")
        else:
            team_form = TeamForm()
            team_member_formset = TeamHasMemberFormSet(initial=[{'team_member' : str(participant.participant_code)}])

        return render(request, 'main_page/register_team.html',
                        {
                            'team_form': team_form,
                            'team_member_formset': team_member_formset,
                            })


    # No need to create form for solo events
    # If event_type is duet or group, then create a form and get the details
    # Note that same form can be used in duet or group events (duet also has team name)
    # Just check the event_type, minimum_team_size, maximum_team_size
    # and render the form accordingly
    # We collect name, email and mobile number of each team member who has not already a participant
    # and first create their user model, then create their participant model (and create
    # participant_code for each participant the same way as done in register_as_participant)
    # Then we do 7 things:
    # 1. We send email to each individual newly made (who was not a participant earlier)
    # participant separately about their participant_code
    # 2. After successful payment, we add each participant to ParticipantHasPaid table
    # 3. We add each participant to ParticipantHasParticipated table
    # 4. We add each participant to TeamHasMember table
    # 5. We create a unique Team Code just like we created unique CA Code (Divyanshu will help)
    # 6. We send email to the whole team about their participation (Divyanshu will take care of the content of the email)
    # 7. Show success page
    # Note: Remember to use TeamForm as a part of the form
    # Note: Give option of registering team member by entering his participant_code so that
    # participants who have already paid for the subcategory do not pay again
    # then we don't need to ask for that user's mobile number and email since he is already registered
    # Also, payment should be calculated by seeing that
    # how many participants of the team have already paid for this even't subcategory
    # Note: Some people might still type email and mobile for participants who have already registered
    # so we need to check each email address and get the associated user and check if he has already paid or not

    # For solo events, just redirect to payment portal, then do 5 things:
    # 1. If user has not already paid for that subcategory, then
    # after successful payment, add the participant to ParticipantHasPaid table
    # 2. Add the participant to ParticipantHasParticipated table
    # 3. Add the participant to TeamHasMember table
    # 5. We send email to the participant about their participation (Divyanshu will take care of the content of the email)
    # 6. Show success page


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
